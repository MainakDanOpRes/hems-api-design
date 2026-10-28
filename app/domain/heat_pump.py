from pydantic import BaseModel, Field

from app.domain.capabilities import DeviceCapabilities
from app.domain.constraints import DeviceConstraintType
from app.domain.device import Device


class HeatPumpState(BaseModel):
    running: bool
    power_kw: float = Field(ge=0)
    indoor_temperature_c: float
    outdoor_temperature_c: float


class HeatPump(Device):
    capabilities: DeviceCapabilities

    state: HeatPumpState

    constraints: list[DeviceConstraintType] = Field(
        default_factory=list
    )