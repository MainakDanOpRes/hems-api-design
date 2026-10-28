"""Define the domain model and properties specific to a home energy storage battery."""

from pydantic import BaseModel, Field

from app.domain.capabilities import DeviceCapabilities
from app.domain.device import Device


class BatteryState(BaseModel):
    soc_percent: float = Field(ge=0, le=100)
    power_kw: float
    status: str


class Battery(Device):
    capacity_kwh: float = Field(gt=0)

    capabilities: DeviceCapabilities
    state: BatteryState
