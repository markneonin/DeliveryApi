from pydantic import BaseModel
from typing import List, Optional, Any


class Courier(BaseModel):
    courier_id: int
    courier_type: str
    regions: List[int]
    working_hours: List[str]


class FullCourierInfo(Courier):
    rating: Optional[float]
    earnings: int


class AssignData(BaseModel):
    orders: List[Any]
    assign_time: Optional[str]
