"""Represent a vehicle and its relevant characteristics for home energy management."""

from pydantic import BaseModel, Field


class Vehicle(BaseModel):
    id: str
    name: str

    battery_capacity_kwh: float = Field(gt=0)

    current_soc_percent: float = Field(
        ge=0,
        le=100,
    )

    target_soc_percent: float = Field(
        ge=0,
        le=100,
    )