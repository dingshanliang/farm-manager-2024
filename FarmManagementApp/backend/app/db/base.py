# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base
from app.models.agri_advice import (AgriAdvice, AgriAdviceRating,
                                    AgriAdviceResponse)
from app.models.farm import Farm
from app.models.farm_activity import FarmActivity
from app.models.field import Field
from app.models.planting_plan import PlantingPlan
from app.models.task import Task
from app.models.user import User
from app.models.weather_forecast import WeatherForecast

# Import other models as needed
