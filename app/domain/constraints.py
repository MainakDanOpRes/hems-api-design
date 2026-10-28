"""Define constraint types and rules that limit or govern device operation."""

from typing import Annotated, Literal
from datetime import datetime
from pydantic import BaseModel, Field, model_validator


class DeviceConstraint(BaseModel):
    type: str
    name: str
    description: str | None = None


class PowerConstraint(DeviceConstraint):
    type: Literal["power"] = "power"

    min_power_kw: float = Field(ge=0)
    max_power_kw: float = Field(gt=0)

    @model_validator(mode="after")
    def validate_power_range(self):
        if self.min_power_kw > self.max_power_kw:
            raise ValueError(
                "min_power_kw must be less than or equal to max_power_kw"
            )

        return self


class BatteryConstraint(DeviceConstraint):
    type: Literal["battery"] = "battery"

    min_soc_percent: float = Field(ge=0, le=100)
    max_soc_percent: float = Field(ge=0, le=100)

    max_charge_kw: float = Field(gt=0)
    max_discharge_kw: float = Field(gt=0)

    @model_validator(mode="after")
    def validate_soc_range(self):
        if self.min_soc_percent > self.max_soc_percent:
            raise ValueError(
                "min_soc_percent must be less than or equal to max_soc_percent"
            )

        return self

class EVChargingConstraint(DeviceConstraint):
    type: Literal["ev_charging"] = "ev_charging"

    max_charge_kw: float = Field(gt=0)


class AvailabilityConstraint(DeviceConstraint):
    type: Literal["availability"] = "availability"

    available_from: datetime
    available_until: datetime

    @model_validator(mode="after")
    def validate_availability_range(self):
        if self.available_from > self.available_until:
            raise ValueError(
                "available_from must be less than or equal to available_until"
            )

        return self

class ThermalConstraint(DeviceConstraint):
    type: Literal["thermal"] = "thermal"

    min_temperature_c: float
    max_temperature_c: float
    target_temperature_c: float

    @model_validator(mode="after")
    def validate_temperature_range(self):
        if self.min_temperature_c > self.max_temperature_c:
            raise ValueError(
                "min_temperature_c must be less than or equal to max_temperature_c"
            )

        if not (
            self.min_temperature_c
            <= self.target_temperature_c
            <= self.max_temperature_c
        ):
            raise ValueError(
                "target_temperature_c must be between "
                "min_temperature_c and max_temperature_c"
            )

        return self

    
DeviceConstraintType = Annotated[
    PowerConstraint
    | BatteryConstraint
    | EVChargingConstraint
    | AvailabilityConstraint
    | ThermalConstraint,
    Field(discriminator="type"),
]

