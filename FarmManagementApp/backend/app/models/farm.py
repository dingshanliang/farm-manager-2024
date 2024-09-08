import enum
import random
from datetime import datetime

from geoalchemy2.shape import to_shape
from shapely.geometry import Point
from sqlalchemy import Column, Date, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, validates

from ..db.base_class import Base


class CropType(enum.Enum):
    WHEAT = "小麦"
    CORN = "玉米"
    RICE = "水稻"
    SOYBEAN = "大豆"
    # 添加更多作物类型...

class ActivityType(enum.Enum):
    PLOWING = "耕作"
    PLANTING = "种植"
    FERTILIZING = "施肥"
    IRRIGATING = "灌溉"
    HARVESTING = "收获"
    # 添加更多活动类型...

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    size = Column(Float)  # 以公顷为单位
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(Date, default=datetime.utcnow)
    updated_at = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 使用字符串引用
    owner = relationship("User", back_populates="farms")
    fields = relationship("Field", back_populates="farm")
    activities = relationship("FarmActivity", back_populates="farm")
    weather_forecasts = relationship("WeatherForecast", back_populates="farm")
    tasks = relationship("Task", back_populates="farm")  # 使用字符串引用
    planting_plans = relationship("PlantingPlan", back_populates="farm")  # 使用字符串引用

    @validates('size')
    def validate_size(self, key, size):
        if size <= 0:
            raise ValueError("农场大小必须大于0")
        return size

    @hybrid_property
    def total_field_size(self):
        return sum(field.size for field in self.fields)

    def __repr__(self):
        return f"<Farm(id={self.id}, name='{self.name}', size={self.size})>"

    @hybrid_property
    def random_coordinate(self):
        if self.fields:
            random_field = random.choice(self.fields)
            shape = to_shape(random_field.geometry)
            if isinstance(shape, Point):
                return shape.x, shape.y
            else:
                point = shape.representative_point()
                return point.x, point.y
        return None, None

    @hybrid_property
    def latitude(self):
        return self.random_coordinate[1]

    @hybrid_property
    def longitude(self):
        return self.random_coordinate[0]