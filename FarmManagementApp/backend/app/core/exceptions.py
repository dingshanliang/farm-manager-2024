from fastapi import HTTPException, status


class FarmNotFoundException(HTTPException):
    def __init__(self, farm_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"农场 ID {farm_id} 未找到"
        )

class FieldNotFoundException(HTTPException):
    def __init__(self, field_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"田地 ID {field_id} 未找到"
        )

class ActivityNotFoundException(HTTPException):
    def __init__(self, activity_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"农事活动 ID {activity_id} 未找到"
        )