"""Define the Home model and validate its identity, time zone, and import/export power limits."""

import math

from pydantic import BaseModel, Field, field_validator


class Home(BaseModel):
    id: str
    name: str
    timezone: str
    max_import_kw: float = Field(gt=0)
    max_export_kw: float = Field(gt=0)

    @field_validator("max_import_kw", "max_export_kw")
    @classmethod
    def power_limits_must_be_finite(cls, value: float) -> float:
        if not math.isfinite(value):
            raise ValueError("Power limits must be finite numbers")
        return value
