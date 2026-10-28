
import pytest
from pydantic import ValidationError

from app.domain.constraints import ThermalConstraint


def test_thermal_constraint_accepts_valid_temperatures():
    constraint = ThermalConstraint(
        name="Living room temperature",
        min_temperature_c=19,
        target_temperature_c=21,
        max_temperature_c=22,
    )

    assert constraint.min_temperature_c == 19
    assert constraint.target_temperature_c == 21
    assert constraint.max_temperature_c == 22


@pytest.mark.parametrize(
    ("min_temp", "target_temp", "max_temp"),
    [
        (19, 23, 22),  # Target above maximum
        (19, 18, 22),  # Target below minimum
        (23, 21, 22),  # Minimum above maximum
    ],
)
def test_thermal_constraint_rejects_invalid_temperatures(
    min_temp,
    target_temp,
    max_temp,
):
    with pytest.raises(ValidationError):
        ThermalConstraint(
            name="Invalid temperature limits",
            min_temperature_c=min_temp,
            target_temperature_c=target_temp,
            max_temperature_c=max_temp,
        )


@pytest.mark.parametrize(
    ("min_temp", "target_temp", "max_temp"),
    [
        (19, 19, 22),  # Target equals minimum
        (19, 22, 22),  # Target equals maximum
        (21, 21, 21),  # All limits equal
    ],
)
def test_thermal_constraint_accepts_boundary_temperatures(
    min_temp,
    target_temp,
    max_temp,
):
    constraint = ThermalConstraint(
        name="Boundary temperature limits",
        min_temperature_c=min_temp,
        target_temperature_c=target_temp,
        max_temperature_c=max_temp,
    )

    assert (
        constraint.min_temperature_c
        <= constraint.target_temperature_c
        <= constraint.max_temperature_c
    )