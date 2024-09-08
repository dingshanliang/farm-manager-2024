# 初始化schemas
from .agri_advice import AgriAdvice, AgriAdviceCreate, AgriAdviceUpdate
from .farm import (Farm, FarmActivity, FarmActivityCreate, FarmActivityUpdate,
                   FarmCreate, FarmUpdate)
from .farm_activity import FarmActivity, FarmActivityCreate, FarmActivityUpdate
from .field import CropType, Field, FieldCreate, FieldUpdate
from .planting_plan import PlantingPlan, PlantingPlanCreate, PlantingPlanUpdate
from .task import Task, TaskCreate, TaskUpdate
from .user import User, UserCreate, UserUpdate

# 如果需要，可以在这里添加 __all__ 来明确指定可以从这个包导入的名称
__all__ = [
    "CropType",
    "Farm", "FarmCreate", "FarmUpdate",
    "FarmActivity", "FarmActivityCreate", "FarmActivityUpdate",
    "PlantingPlan", "PlantingPlanCreate", "PlantingPlanUpdate",
    # ... 其他需要导出的名称
]
