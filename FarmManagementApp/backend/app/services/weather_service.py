from datetime import datetime, timedelta

import requests
from sqlalchemy.orm import Session

from ..crud.weather import weather as weather_crud
from ..models.farm import Farm
from ..schemas.weather import WeatherForecastCreate

API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # 替换为您的 API 密钥
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

def fetch_and_store_weather(db: Session, farm: Farm):
    if not farm.fields:
        raise ValueError("Farm has no fields")

    lat, lon = farm.random_coordinate
    if lat is None or lon is None:
        raise ValueError("Unable to determine farm coordinates")

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "cnt": 40  # 5 天预报，每天 8 个时间点
    }
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        forecasts = []
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).date()
            forecast = WeatherForecastCreate(
                farm_id=farm.id,
                date=date,
                temperature_high=item['main']['temp_max'],
                temperature_low=item['main']['temp_min'],
                precipitation=item['rain']['3h'] if 'rain' in item else 0,
                humidity=item['main']['humidity'],
                wind_speed=item['wind']['speed'],
                wind_direction=item['wind']['deg'],
                description=item['weather'][0]['description']
            )
            forecasts.append(forecast)

        # 删除旧的天气预报
        weather_crud.remove_old_forecasts(db, farm_id=farm.id)

        # 存储新的天气预报
        for forecast in forecasts:
            weather_crud.create(db, obj_in=forecast)

    else:
        raise Exception(f"Failed to fetch weather data: {data['message']}")

def update_weather_for_all_farms(db: Session):
    farms = db.query(Farm).all()
    for farm in farms:
        fetch_and_store_weather(db, farm)