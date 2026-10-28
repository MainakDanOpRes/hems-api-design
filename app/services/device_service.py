"""Implement device-related use cases and coordinate device operations with the required repositories."""

from typing import Protocol
from uuid import uuid4

from pydantic import BaseModel, Field

from app.domain.constraints import DeviceConstraintType
from app.domain.device import Device, DeviceStatus, DeviceType
from app.domain.home import Home
from app.services.exceptions import DeviceNotFoundError, HomeNotFoundError


class DeviceRegistrationData(BaseModel):
    name: str
    type: DeviceType
    manufacturer: str
    model: str
    status: DeviceStatus = DeviceStatus.OFFLINE
    constraints: list[DeviceConstraintType] = Field(
        default_factory=list
    )


class HomeRepository(Protocol):
    def get_by_id(self, home_id: str) -> Home | None:
        ...


class DeviceRepository(Protocol):
    def save(self, device: Device) -> Device:
        ...

    def get_by_id(self, device_id: str) -> Device | None:
        ...

    def update(self, device: Device) -> Device:
        ...


class DeviceService:
    def __init__(
        self,
        home_repository: HomeRepository,
        device_repository: DeviceRepository,
    ) -> None:
        self.home_repository = home_repository
        self.device_repository = device_repository

    def register_device(
        self,
        home_id: str,
        data: DeviceRegistrationData,
    ) -> Device:
        home = self.home_repository.get_by_id(home_id)

        if home is None:
            raise HomeNotFoundError(f"Home '{home_id}' not found")

        device = Device(
            id=str(uuid4()),
            home_id=home.id,
            name=data.name,
            type=data.type,
            manufacturer=data.manufacturer,
            model=data.model,
            status=data.status,
            constraints=data.constraints,
        )

        return self.device_repository.save(device)

    def get_device(self, device_id: str) -> Device:
        device = self.device_repository.get_by_id(device_id)

        if device is None:
            raise DeviceNotFoundError(
                f"Device '{device_id}' not found"
            )

        return device

    def update_device_status(
        self,
        device_id: str,
        status: DeviceStatus,
    ) -> Device:
        device = self.get_device(device_id)

        updated_device = device.model_copy(
            update={"status": status}
        )

        return self.device_repository.update(updated_device)