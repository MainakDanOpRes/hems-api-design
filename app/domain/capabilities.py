"""Represent the capabilities that determine which operations an energy device can perform."""

from pydantic import BaseModel


class DeviceCapabilities(BaseModel):
    can_consume: bool = False
    can_generate: bool = False
    can_store: bool = False
    can_control_power: bool = False
    can_start: bool = False
    can_stop: bool = False