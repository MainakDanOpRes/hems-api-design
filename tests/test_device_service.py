"""Test device-service use cases, status updates, and repository interactions."""

import pytest

from app.domain.device import DeviceStatus, DeviceType
from app.domain.home import Home
from app.services.device_service import (
    DeviceRegistrationData,
    DeviceService,
)
from app.services.exceptions import HomeNotFoundError, DeviceNotFoundError

class FakeHomeRepository:
    def __init__(self, homes: list[Home]):
        self.homes = {home.id: home for home in homes}

    def get_by_id(self, home_id: str) -> Home | None:
        return self.homes.get(home_id)

    def update(self, device):
        self.devices[device.id] = device
        return device


class FakeDeviceRepository:
    def __init__(self):
        self.devices = {}
        self.save_calls = 0
        self.update_calls = 0

    def save(self, device):
        self.save_calls += 1
        self.devices[device.id] = device
        return device

    def get_by_id(self, device_id: str):
        return self.devices.get(device_id)

    def update(self, device):
        self.update_calls += 1
        self.devices[device.id] = device
        return device


@pytest.fixture
def home():
    return Home(
        id="home-1",
        name="My Home",
        timezone="Europe/Paris",
        max_import_kw=12.0,
        max_export_kw=6.0,
    )


@pytest.fixture
def device_service(home):
    home_repository = FakeHomeRepository([home])
    device_repository = FakeDeviceRepository()

    service = DeviceService(
        home_repository=home_repository,
        device_repository=device_repository,
    )

    return service, device_repository


def test_register_device_success(device_service, home):
    service, device_repository = device_service

    data = DeviceRegistrationData(
        name="Smart Meter",
        type=DeviceType.SMART_METER,
        manufacturer="Example Manufacturer",
        model="Meter-100",
    )

    device = service.register_device(home.id, data)

    assert device.home_id == home.id
    assert device.name == "Smart Meter"
    assert device.id
    assert len(device_repository.devices) == 1
    assert device_repository.devices[device.id] == device
    assert device_repository.save_calls == 1


def test_register_device_home_not_found(device_service):
    service, device_repository = device_service

    data = DeviceRegistrationData(
        name="Smart Meter",
        type=DeviceType.SMART_METER,
        manufacturer="Example Manufacturer",
        model="Meter-100",
    )

    with pytest.raises(
        HomeNotFoundError,
        match="Home 'missing-home' not found",
    ):
        service.register_device("missing-home", data)

    assert device_repository.save_calls == 0
    assert device_repository.devices == {}


def test_register_device_preserves_device_data(device_service):
    service, _ = device_service

    data = DeviceRegistrationData(
        name="Solar Inverter",
        type=DeviceType.SOLAR_PV,
        manufacturer="SolarCo",
        model="Inverter-X",
        status=DeviceStatus.ONLINE,
    )

    device = service.register_device("home-1", data)

    assert device.name == "Solar Inverter"
    assert device.type == DeviceType.SOLAR_PV
    assert device.manufacturer == "SolarCo"
    assert device.model == "Inverter-X"
    assert device.status == DeviceStatus.ONLINE


def test_get_device_success(device_service, home):
    service, device_repository = device_service

    data = DeviceRegistrationData(
        name="Smart Meter",
        type=DeviceType.SMART_METER,
        manufacturer="Example Manufacturer",
        model="Meter-100",
    )

    registered_device = service.register_device(home.id, data)

    device = service.get_device(registered_device.id)

    assert device == registered_device
    assert device_repository.devices[device.id] == device


def test_get_device_not_found(device_service):
    service, _ = device_service

    with pytest.raises(
        DeviceNotFoundError,
        match="Device 'missing-device' not found",
    ):
        service.get_device("missing-device")


def test_update_device_status_success(device_service, home):
    service, device_repository = device_service

    data = DeviceRegistrationData(
        name="Smart Meter",
        type=DeviceType.SMART_METER,
        manufacturer="Example Manufacturer",
        model="Meter-100",
    )

    device = service.register_device(home.id, data)

    updated_device = service.update_device_status(
        device.id,
        DeviceStatus.ONLINE,
    )

    assert updated_device.status == DeviceStatus.ONLINE
    assert device_repository.devices[device.id].status == DeviceStatus.ONLINE
    assert device_repository.devices[device.id] == updated_device
    assert device_repository.update_calls == 1


def test_update_device_status_not_found(device_service):
    service, device_repository = device_service

    with pytest.raises(
        DeviceNotFoundError,
        match="Device 'missing-device' not found",
    ):
        service.update_device_status(
            "missing-device",
            DeviceStatus.ONLINE,
        )

    assert device_repository.devices == {}


def test_update_device_status_success(device_service, home):
    service, device_repository = device_service

    data = DeviceRegistrationData(
        name="Smart Meter",
        type=DeviceType.SMART_METER,
        manufacturer="Example Manufacturer",
        model="Meter-100",
    )

    device = service.register_device(home.id, data)

    original_id = device.id
    original_home_id = device.home_id
    original_name = device.name
    original_type = device.type
    original_manufacturer = device.manufacturer
    original_model = device.model

    updated_device = service.update_device_status(
        device.id,
        DeviceStatus.ONLINE,
    )

    assert updated_device.status == DeviceStatus.ONLINE

    assert updated_device.id == original_id
    assert updated_device.home_id == original_home_id
    assert updated_device.name == original_name
    assert updated_device.type == original_type
    assert updated_device.manufacturer == original_manufacturer
    assert updated_device.model == original_model

    assert device_repository.devices[device.id] == updated_device



def test_update_device_status_does_not_mutate_original(
    device_service,
    home,
):
    service, device_repository = device_service

    data = DeviceRegistrationData(
        name="Smart Meter",
        type=DeviceType.SMART_METER,
        manufacturer="Example Manufacturer",
        model="Meter-100",
    )

    device = service.register_device(home.id, data)
    original_status = device.status

    updated_device = service.update_device_status(
        device.id,
        DeviceStatus.ONLINE,
    )

    assert device.status == original_status
    assert updated_device.status == DeviceStatus.ONLINE
    assert updated_device is not device


def test_update_device_status_preserves_original_if_persistence_fails(
    device_service,
    home,
):
    service, device_repository = device_service

    data = DeviceRegistrationData(
        name="Smart Meter",
        type=DeviceType.SMART_METER,
        manufacturer="Example Manufacturer",
        model="Meter-100",
    )

    device = service.register_device(home.id, data)
    original_status = device.status

    def failing_update(updated_device):
        raise RuntimeError("Database write failed")

    device_repository.update = failing_update

    with pytest.raises(RuntimeError, match="Database write failed"):
        service.update_device_status(
            device.id,
            DeviceStatus.ONLINE,
        )

    assert device.status == original_status
