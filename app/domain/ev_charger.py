from pydantic import BaseModel, Field

from app.domain.capabilities import DeviceCapabilities
from app.domain.device import Device
from app.domain.constraints import DeviceConstraintType


class EVChargerState(BaseModel):
    connected: bool
    charging: bool
    power_kw: float = Field(ge=0)


class EVCharger(Device):
    capabilities: DeviceCapabilities

    state: EVChargerState

    constraints: list[DeviceConstraintType] = Field(
        default_factory=list
    )