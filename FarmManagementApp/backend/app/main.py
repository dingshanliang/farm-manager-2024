from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .api import api_router  # 修改这行
from .core.config import settings
from .core.logger import main_logger
from .core.security import (authenticate_user, create_access_token,
                            get_current_active_user)
from .crud import user as user_crud
from .db.base import Base  # 修改这行
from .db.session import engine, get_db
from .schemas import user as user_schemas

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# 设置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 册路由
app.include_router(api_router, prefix="/api/v1")

@app.post("/token", response_model=user_schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        main_logger.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    main_logger.info(f"User {user.email} logged in successfully")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=user_schemas.User)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    return user_crud.create_user(db=db, user=user)

@app.get("/users/me/", response_model=user_schemas.User)
async def read_users_me(current_user: user_schemas.User = Depends(get_current_active_user)):
    return current_user

@app.get("/")
async def root():
    return {"message": "欢迎使用数字农服软件平台"}

# 添加这个函数来创建数据库表
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

# 注释掉这些行
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from redis import asyncio as aioredis

# @app.on_event("startup")
# async def startup():
#     redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")