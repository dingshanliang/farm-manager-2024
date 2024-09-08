from datetime import date
from typing import Optional

from pydantic import BaseModel


class WeatherForecastBase(BaseModel):
    date: date
    temperature_high: float
    temperature_low: float
    precipitation: float
    humidity: float
    wind_speed: float
    wind_direction: str
    description: str

class WeatherForecastCreate(WeatherForecastBase):
    farm_id: int

class WeatherForecast(WeatherForecastBase):
    id: int
    farm_id: int

    class Config:
        orm_mode = True