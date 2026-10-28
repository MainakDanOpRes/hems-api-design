
from app.repositories.memory import (
    InMemoryDeviceRepository,
    InMemoryHomeRepository,
)
from app.services.device_service import DeviceService
from app.services.home_service import HomeService


home_repository = InMemoryHomeRepository()
device_repository = InMemoryDeviceRepository()


def get_device_service() -> DeviceService:
    return DeviceService(
        home_repository=home_repository,
        device_repository=device_repository,
    )

def get_home_service() -> HomeService:

    return HomeService(home_repository=home_repository)