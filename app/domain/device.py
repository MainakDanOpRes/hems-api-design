"""Define device types, operational statuses, and the common Device model."""

from enum import Enum

from pydantic import BaseModel, Field
from app.domain.constraints import DeviceConstraintType


class DeviceType(str, Enum):
    SOLAR_PV = "solar_pv"
    BATTERY = "battery"
    EV_CHARGER = "ev_charger"
    HEAT_PUMP = "heat_pump"
    SMART_METER = "smart_meter"
    WASHING_MACHINE = "washing_machine"


class DeviceStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"


class Device(BaseModel):
    id: str
    home_id: str
    name: str
    type: DeviceType
    manufacturer: str
    model: str
    status: DeviceStatus
    constraints: list[DeviceConstraintType] = Field(default_factory=list)