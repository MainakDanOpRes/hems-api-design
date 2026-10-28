"""Define HTTP endpoints for registering devices, retrieving devices, and updating their status."""

from pydantic import BaseModel, Field
from fastapi import status
from fastapi import APIRouter, Depends, HTTPException


from app.api.validation import NameField
from app.domain.device import Device, DeviceType
from app.services.device_service import DeviceService, DeviceRegistrationData
from app.services.exceptions import DeviceNotFoundError, HomeNotFoundError
from app.api.dependencies import get_device_service


router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/{device_id}", response_model=Device)
def get_device(
    device_id: str,
    service: DeviceService = Depends(get_device_service),
) -> Device:
    try:
        return service.get_device(device_id)
    except DeviceNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


class DeviceRegistrationRequest(BaseModel):
    name: NameField
    type: DeviceType
    manufacturer: NameField
    model: NameField
        


@router.post(
    "/homes/{home_id}",
    response_model=Device,
    status_code=status.HTTP_201_CREATED,
)
def register_device(
    home_id: str,
    data: DeviceRegistrationRequest,
    service: DeviceService = Depends(get_device_service),
) -> Device:
    registration_data = DeviceRegistrationData(
        name=data.name,
        type=data.type,
        manufacturer=data.manufacturer,
        model=data.model,
    )

    try:
        return service.register_device(home_id, registration_data)
    except HomeNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
