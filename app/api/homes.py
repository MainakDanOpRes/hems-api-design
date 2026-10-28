"""Define HTTP endpoints for registering homes and retrieving a home by its ID."""

from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field, field_validator
import math


from app.api.validation import NameField, TimezoneField
from app.api.dependencies import get_home_service
from app.domain.home import Home
from app.services.home_service import HomeRegistrationData, HomeService
from app.services.exceptions import HomeNotFoundError


router = APIRouter(prefix="/homes", tags=["homes"])


class HomeRegistrationRequest(BaseModel):
    name: NameField
    timezone: TimezoneField
    max_import_kw: float = Field(gt=0)
    max_export_kw: float = Field(gt=0)
    @field_validator("max_import_kw", "max_export_kw")
    @classmethod
    def power_limits_must_be_finite(cls, value: float) -> float:
        if not math.isfinite(value):
            raise ValueError("Power limits must be finite numbers")
        return value



@router.post(
    "",
    response_model=Home,
    status_code=status.HTTP_201_CREATED,
)
def register_home(
    data: HomeRegistrationRequest,
    service: HomeService = Depends(get_home_service),
) -> Home:
    registration_data = HomeRegistrationData(
        name=data.name,
        timezone=data.timezone,
        max_import_kw=data.max_import_kw,
        max_export_kw=data.max_export_kw,
    )
    return service.register_home(registration_data)


@router.get("/{home_id}", response_model=Home)
def get_home(
    home_id: str,
    service: HomeService = Depends(get_home_service),
) -> Home:
    try:
        return service.get_home(home_id)
    except HomeNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
