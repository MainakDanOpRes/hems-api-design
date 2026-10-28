
import pytest
from pydantic import ValidationError
from app.domain.constraints import BatteryConstraint


def test_battery_constraint_accepts_valid_soc_range():
    constraint = BatteryConstraint(
        name="Battery operating limits",
        min_soc_percent=10,
        max_soc_percent=95,
        max_charge_kw=5,
        max_discharge_kw=5,
    )

    assert constraint.min_soc_percent == 10
    assert constraint.max_soc_percent == 95


def test_battery_constraint_rejects_invalid_soc_range():
    with pytest.raises(ValidationError) as exc_info:
        BatteryConstraint(
            name="Invalid battery limits",
            min_soc_percent=95,
            max_soc_percent=10,
            max_charge_kw=5,
            max_discharge_kw=5,
        )
    assert "min_soc_percent" in str(exc_info.value)


def test_battery_constraint_accepts_equal_soc_limits():
    constraint = BatteryConstraint(
        name="Fixed SOC limit",
        min_soc_percent=50,
        max_soc_percent=50,
        max_charge_kw=5,
        max_discharge_kw=5,
    )

    assert constraint.min_soc_percent == constraint.max_soc_percent