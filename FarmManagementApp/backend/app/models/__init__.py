# 初始化数据库模型
from .agri_advice import AgriAdvice, AgriAdviceRating, AgriAdviceResponse
from .farm import Farm
from .farm_activity import FarmActivity
from .field import Field
from .planting_plan import PlantingPlan
from .task import Task
from .user import User
from .weather_forecast import WeatherForecast

# 如果需要，可以在这里添加 __all__ 来明确指定可以从这个包导入的名称
__all__ = [
    "User",
    "Farm",
    "Field",
    "PlantingPlan",
    "Task",
    "FarmActivity",
    "WeatherForecast",
    "AgriAdvice",
    "AgriAdviceResponse",
    "AgriAdviceRating"
]
