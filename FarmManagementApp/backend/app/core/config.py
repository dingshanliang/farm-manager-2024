from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 你的设置项...
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PROJECT_NAME: str = "数字农服软件平台"
    PROJECT_VERSION: str = "1.0.0"
    ALLOWED_ORIGINS: list = ["http://localhost", "http://localhost:3000"]  # 添加允许的源

    class Config:
        env_file = ".env"

settings = Settings()