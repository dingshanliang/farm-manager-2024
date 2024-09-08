from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db.base_class import Base


class WeatherForecast(Base):
    __tablename__ = "weather_forecasts"
    __table_args__ = {'extend_existing': True}  # 添加这行

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    date = Column(Date)
    temperature_high = Column(Float)
    temperature_low = Column(Float)
    precipitation = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(String)
    description = Column(String)

    farm = relationship("Farm", back_populates="weather_forecasts")