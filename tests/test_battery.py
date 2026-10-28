
import pytest

from pydantic import ValidationError

from app.domain.battery import Battery, BatteryState
from app.domain.capabilities import DeviceCapabilities
from app.domain.constraints import BatteryConstraint
from app.domain.device import DeviceStatus, DeviceType


def create_battery(soc_percent: float = 73, capacity_kwh: float = 10) -> Battery:
    return Battery(
        id="battery_001",
        home_id="home_001",
        name="Home Battery",
        type=DeviceType.BATTERY,
        manufacturer="Tesla",
        model="Powerwall",
        status=DeviceStatus.ONLINE,
        capacity_kwh=capacity_kwh,
        capabilities=DeviceCapabilities(
            can_consume=True,
            can_generate=True,
            can_store=True,
            can_control_power=True,
        ),
        state=BatteryState(
            soc_percent=soc_percent,
            power_kw=3,
            status="charging",
        ),
        constraints=[
            BatteryConstraint(
                name="Battery operating limits",
                min_soc_percent=10,
                max_soc_percent=95,
                max_charge_kw=5,
                max_discharge_kw=5,
            )
        ],
    )

@pytest.mark.parametrize("soc_percent", [20, 30, 50, 70, 90, 100])
def test_battery_accepts_valid_soc(soc_percent):
    battery = create_battery(soc_percent)
    assert battery.state.soc_percent == soc_percent


@pytest.mark.parametrize("soc_percent", [101, 120, -1, -50])
def test_battery_rejects_invalid_soc(soc_percent):
    with pytest.raises(ValidationError) as exc_info:
        create_battery(soc_percent=soc_percent)

    assert "soc_percent" in str(exc_info.value)

@pytest.mark.parametrize("soc_percent", [0, 100])
def test_battery_accepts_boundary_soc(soc_percent):
    battery = create_battery(soc_percent=soc_percent)
    assert battery.state.soc_percent == soc_percent

@pytest.mark.parametrize("capacity_kwh", [0, -1, -10])
def test_battery_rejects_invalid_capacity(capacity_kwh):
    with pytest.raises(ValidationError) as exc_info:
        create_battery(capacity_kwh=capacity_kwh)

    assert "capacity_kwh" in str(exc_info.value)

@pytest.mark.parametrize("capacity_kwh", [10, 20, 100])
def test_battery_accepts_positive_capacity(capacity_kwh):
    battery = create_battery(capacity_kwh=capacity_kwh)
    assert battery.capacity_kwh == capacity_kwh