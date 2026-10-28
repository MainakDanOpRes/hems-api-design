"""Test API endpoints, response codes, request validation, and error handling."""
    
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_device_not_found():
    response = client.get("/devices/nonexistent-device")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Device 'nonexistent-device' not found"
    }


def test_register_device_home_not_found():
    response = client.post(
        "/devices/homes/nonexistent-home",
        json={
            "name": "Smart Meter",
            "type": "smart_meter",
            "manufacturer": "Example Manufacturer",
            "model": "Meter-100",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Home 'nonexistent-home' not found"
    }

def test_register_home_success():
    response = client.post(
        "/homes",
        json={
            "name": "My Home",
            "timezone": "Europe/Paris",
            "max_import_kw": 12.0,
            "max_export_kw": 6.0,
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["name"] == "My Home"
    assert body["timezone"] == "Europe/Paris"
    assert body["max_import_kw"] == 12.0
    assert body["max_export_kw"] == 6.0
    assert isinstance(body["id"], str)
    assert body["id"]


def test_create_home_register_device_and_retrieve_it():
    home_response = client.post(
        "/homes",
        json={
            "name": "Energy Smart Home",
            "timezone": "Europe/Paris",
            "max_import_kw": 12.0,
            "max_export_kw": 6.0,
        },
    )

    assert home_response.status_code == 201
    home_id = home_response.json()["id"]

    device_response = client.post(
        f"/devices/homes/{home_id}",
        json={
            "name": "Smart Meter",
            "type": "smart_meter",
            "manufacturer": "Example Manufacturer",
            "model": "Meter-100",
        },
    )

    assert device_response.status_code == 201
    device = device_response.json()

    assert device["home_id"] == home_id
    assert device["name"] == "Smart Meter"
    assert device["type"] == "smart_meter"
    assert device["status"] == "offline"

    retrieval_response = client.get(
        f"/devices/{device['id']}"
    )

    assert retrieval_response.status_code == 200
    assert retrieval_response.json() == device


def test_register_home_rejects_invalid_power_limit():
    response = client.post(
        "/homes",
        json={
            "name": "Invalid Home",
            "timezone": "Europe/Paris",
            "max_import_kw": -1.0,
            "max_export_kw": 6.0,
        },
    )

    assert response.status_code == 422


def test_register_device_rejects_invalid_device_type():
    response = client.post(
        "/devices/homes/some-home",
        json={
            "name": "Unknown Device",
            "type": "invalid_type",
            "manufacturer": "Example Manufacturer",
            "model": "Model-100",
        },
    )

    assert response.status_code == 422


def test_invalid_home_request_does_not_create_home():
    from app.api.dependencies import home_repository

    homes_before = len(home_repository.homes)

    response = client.post(
        "/homes",
        json={
            "name": "Invalid Home",
            "timezone": "Europe/Paris",
            "max_import_kw": -1.0,
            "max_export_kw": 6.0,
        },
    )

    assert response.status_code == 422
    assert len(home_repository.homes) == homes_before

def test_register_device_rejects_empty_name():
    response = client.post(
        "/devices/homes/some-home",
        json={
            "name": "",
            "type": "smart_meter",
            "manufacturer": "Example Manufacturer",
            "model": "Meter-100",
        },
    )

    assert response.status_code == 422


def test_register_home_rejects_empty_name():
    response = client.post(
        "/homes",
        json={
            "name": "",
            "timezone": "Europe/Paris",
            "max_import_kw": 12.0,
            "max_export_kw": 6.0,
        },
    )

    assert response.status_code == 422

def test_register_home_rejects_whitespace_name():
    response = client.post(
        "/homes",
        json={
            "name": "   ",
            "timezone": "Europe/Paris",
            "max_import_kw": 12.0,
            "max_export_kw": 6.0,
        },
    )

    assert response.status_code == 422


def test_register_device_rejects_whitespace_name():
    response = client.post(
        "/devices/homes/some-home",
        json={
            "name": "   ",
            "type": "smart_meter",
            "manufacturer": "Example Manufacturer",
            "model": "Meter-100",
        },
    )

    assert response.status_code == 422


def test_register_home_strips_name_whitespace():
    response = client.post(
        "/homes",
        json={
            "name": "  My Home  ",
            "timezone": "Europe/Paris",
            "max_import_kw": 12.0,
            "max_export_kw": 6.0,
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "My Home"



def test_register_device_strips_name_whitespace():
    home_response = client.post(
        "/homes",
        json={
            "name": "Device Test Home",
            "timezone": "Europe/Paris",
            "max_import_kw": 12.0,
            "max_export_kw": 6.0,
        },
    )
    home_id = home_response.json()["id"]

    response = client.post(
        f"/devices/homes/{home_id}",
        json={
            "name": "  Kitchen Meter  ",
            "type": "smart_meter",
            "manufacturer": "Example Manufacturer",
            "model": "Meter-100",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Kitchen Meter"


def test_register_device_rejects_blank_manufacturer():
    home_response = client.post(
        "/homes",
        json={
            "name": "Manufacturer Test Home",
            "timezone": "Europe/Paris",
            "max_import_kw": 12.0,
            "max_export_kw": 6.0,
        },
    )
    home_id = home_response.json()["id"]

    response = client.post(
        f"/devices/homes/{home_id}",
        json={
            "name": "Kitchen Meter",
            "type": "smart_meter",
            "manufacturer": "   ",
            "model": "Meter-100",
        },
    )

    assert response.status_code == 422


def test_register_home_rejects_invalid_timezone():
    response = client.post(
        "/homes",
        json={
            "name": "Timezone Test Home",
            "timezone": "Not/A_Timezone",
            "max_import_kw": 12.0,
            "max_export_kw": 6.0,
        },
    )

    assert response.status_code == 422


def test_register_home_strips_timezone_whitespace():
    response = client.post(
        "/homes",
        json={
            "name": "Timezone Whitespace Test",
            "timezone": " Europe/Paris ",
            "max_import_kw": 12.0,
            "max_export_kw": 6.0,
        },
    )

    assert response.status_code == 201
    assert response.json()["timezone"] == "Europe/Paris"


def test_register_home_rejects_infinite_import_limit():
    response = client.post(
        "/homes",
        json={
            "name": "Invalid Power Limit Home",
            "timezone": "Europe/Paris",
            "max_import_kw": "Infinity",
            "max_export_kw": 6.0,
        },
    )

    assert response.status_code == 422


def test_get_home_returns_existing_home():
    create_response = client.post(
        "/homes",
        json={
            "name": "Retrieval Test Home",
            "timezone": "Europe/Paris",
            "max_import_kw": 12.0,
            "max_export_kw": 6.0,
        },
    )
    home_id = create_response.json()["id"]

    response = client.get(f"/homes/{home_id}")

    assert response.status_code == 200
    assert response.json()["id"] == home_id
    assert response.json()["name"] == "Retrieval Test Home"


def test_get_home_returns_404_when_home_does_not_exist():
    response = client.get("/homes/home-404")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_get_home_devices_returns_devices_for_home():
    home_response = client.post(
        "/homes",
        json={
            "name": "Device List Home",
            "timezone": "Europe/Paris",
            "max_import_kw": 12.0,
            "max_export_kw": 6.0,
        },
    )
    home_id = home_response.json()["id"]

    device_response = client.post(
        f"/devices/homes/{home_id}",
        json={
            "name": "Living Room Meter",
            "type": "smart_meter",
            "manufacturer": "Example",
            "model": "Meter-1",
        },
    )
    assert device_response.status_code == 201

    response = client.get(f"/homes/{home_id}/devices")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Living Room Meter"
    assert response.json()[0]["home_id"] == home_id


def test_get_home_devices_returns_empty_list_when_home_has_no_devices():
    home_response = client.post(
        "/homes",
        json={
            "name": "Empty Device List Home",
            "timezone": "Europe/Paris",
            "max_import_kw": 12.0,
            "max_export_kw": 6.0,
        },
    )
    home_id = home_response.json()["id"]

    response = client.get(f"/homes/{home_id}/devices")

    assert response.status_code == 200
    assert response.json() == []


def test_get_home_devices_returns_404_for_unknown_home():
    response = client.get("/homes/home-404/devices")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_update_device_status():
    home_response = client.post(
        "/homes",
        json={
            "name": "Status Test Home",
            "timezone": "Europe/Paris",
            "max_import_kw": 12.0,
            "max_export_kw": 6.0,
        },
    )
    home_id = home_response.json()["id"]

    device_response = client.post(
        f"/devices/homes/{home_id}",
        json={
            "name": "Test Meter",
            "type": "smart_meter",
            "manufacturer": "Example",
            "model": "Meter-1",
        },
    )
    device_id = device_response.json()["id"]

    response = client.patch(
        f"/devices/{device_id}/status",
        json={"status": "online"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_update_device_status_returns_404_for_unknown_device():
    response = client.patch(
        "/devices/device-404/status",
        json={"status": "online"},
    )

    assert response.status_code == 404


def test_update_device_status_rejects_invalid_status():
    response = client.patch(
        "/devices/device-404/status",
        json={"status": "sleeping"},
    )

    assert response.status_code == 422