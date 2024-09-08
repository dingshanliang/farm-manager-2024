from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..crud import weather as weather_crud
from ..database import get_db
from ..models.farm import Farm
from ..schemas import weather as weather_schemas
from ..services.weather_service import fetch_and_store_weather

router = APIRouter()

@router.post("/farms/{farm_id}/weather/", response_model=weather_schemas.WeatherForecast)
def create_weather_forecast(farm_id: int, forecast: weather_schemas.WeatherForecastCreate, db: Session = Depends(get_db)):
    return weather_crud.create_weather_forecast(db=db, forecast=forecast)

@router.get("/farms/{farm_id}/weather/", response_model=List[weather_schemas.WeatherForecast])
def read_weather_forecasts(farm_id: int, skip: int = 0, limit: int = 7, db: Session = Depends(get_db)):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    
    if not farm.fields:
        raise HTTPException(status_code=400, detail="Farm has no fields")
    
    # 获取并存储最新的天气数据
    fetch_and_store_weather(db, farm)
    
    # 从数据库中读取天气预报
    forecasts = weather_crud.get_weather_forecasts(db, farm_id=farm_id, skip=skip, limit=limit)
    return forecasts