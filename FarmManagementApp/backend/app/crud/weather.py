from typing import List

from sqlalchemy.orm import Session

from ..models.weather import WeatherForecast
from ..schemas.weather import WeatherForecastCreate
from .base import CRUDBase


class CRUDWeather(CRUDBase[WeatherForecast, WeatherForecastCreate, WeatherForecastCreate]):
    def get_weather_forecasts(self, db: Session, *, farm_id: int, skip: int = 0, limit: int = 7) -> List[WeatherForecast]:
        return db.query(WeatherForecast).filter(WeatherForecast.farm_id == farm_id).order_by(WeatherForecast.date).offset(skip).limit(limit).all()

    def remove_old_forecasts(self, db: Session, *, farm_id: int):
        db.query(WeatherForecast).filter(WeatherForecast.farm_id == farm_id).delete()
        db.commit()

weather = CRUDWeather(WeatherForecast)