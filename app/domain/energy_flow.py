from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class EnergyNodeType(str, Enum):
    GRID = "grid"
    HOME = "home"
    DEVICE = "device"


class EnergyNode(BaseModel):
    id: str
    type: EnergyNodeType


class EnergyFlow(BaseModel):
    id: str
    home_id: str
    timestamp: datetime

    source: EnergyNode
    destination: EnergyNode

    power_kw: float = Field(ge=0)