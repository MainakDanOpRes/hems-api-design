
from app.domain.device import Device
from app.domain.home import Home


class InMemoryHomeRepository:
    def __init__(self) -> None:
        self.homes: dict[str, Home] = {}

    def save(self, home: Home) -> Home:
        self.homes[home.id] = home
        return home

    def get_by_id(self, home_id: str) -> Home | None:
        return self.homes.get(home_id)


class InMemoryDeviceRepository:
    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    def save(self, device: Device) -> Device:
        self.devices[device.id] = device
        return device

    def get_by_id(self, device_id: str) -> Device | None:
        return self.devices.get(device_id)

    def update(self, device: Device) -> Device:
        self.devices[device.id] = device
        return device
