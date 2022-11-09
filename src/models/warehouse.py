from enum import Enum
from pydantic import BaseModel
from src.models.placement import Placement
from decimal import Decimal

class Status(Enum):
    available = 'Доступен'
    notavailable = 'Не доступен'
    write_off = 'Списан'

class WarehouseItem(BaseModel):
    id: int
    name: str
    cost: Decimal
    country: str
    developer: str
    color: str
    type: str
    status: Status
    placement: Placement
