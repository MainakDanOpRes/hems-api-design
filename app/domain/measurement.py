"""Represent measured energy-system values, including their associated units and measurement context."""

from datetime import datetime

from pydantic import BaseModel, Field


class Measurement(BaseModel):
    id: str
    device_id: str
    timestamp: datetime

    power_kw: float | None = None
    energy_kwh: float | None = None

    soc_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )