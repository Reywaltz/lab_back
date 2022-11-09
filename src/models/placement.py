from enum import Enum

from pydantic import BaseModel, Field

class Placement(BaseModel):
    id: int
    occupied: bool
