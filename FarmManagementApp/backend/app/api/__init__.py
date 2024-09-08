from fastapi import APIRouter

from .activity import router as activity_router
from .agri_advice import router as agri_advice_router
from .farm import router as farm_router
from .planting_plan import router as planting_plan_router
from .task import router as task_router
from .weather import router as weather_forecast_router

api_router = APIRouter()
api_router.include_router(farm_router, prefix="/farms", tags=["farms"])
api_router.include_router(activity_router, prefix="/activities", tags=["activities"])
api_router.include_router(task_router, prefix="/tasks", tags=["tasks"])
api_router.include_router(planting_plan_router, prefix="/planting-plans", tags=["planting plans"])
api_router.include_router(agri_advice_router, prefix="/agri-advices", tags=["agricultural advices"])
api_router.include_router(weather_forecast_router, prefix="/weather-forecasts", tags=["weather forecasts"])