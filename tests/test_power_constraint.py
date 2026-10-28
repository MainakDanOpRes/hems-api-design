"""Test constraints that limit electrical power."""

import pytest
from pydantic import ValidationError

from app.domain.constraints import PowerConstraint


def test_power_constraint_accepts_valid_range():
    constraint = PowerConstraint(
        name="EV charger power limits",
        min_power_kw=0,
        max_power_kw=7.4,
    )

    assert constraint.min_power_kw == 0
    assert constraint.max_power_kw == 7.4


def test_power_constraint_accepts_equal_limits():
    constraint = PowerConstraint(
        name="Fixed power",
        min_power_kw=5,
        max_power_kw=5,
    )

    assert constraint.min_power_kw == constraint.max_power_kw


@pytest.mark.parametrize(
    ("min_power_kw", "max_power_kw"),
    [
        (8, 7.4),
        (10, 5),
    ],
)
def test_power_constraint_rejects_invalid_range(
    min_power_kw,
    max_power_kw,
):
    with pytest.raises(ValidationError):
        PowerConstraint(
            name="Invalid power limits",
            min_power_kw=min_power_kw,
            max_power_kw=max_power_kw,
        )


@pytest.mark.parametrize("max_power_kw", [0, -1])
def test_power_constraint_rejects_nonpositive_max_power(
    max_power_kw,
):
    with pytest.raises(ValidationError):
        PowerConstraint(
            name="Invalid maximum power",
            min_power_kw=0,
            max_power_kw=max_power_kw,
        )


def test_power_constraint_rejects_negative_minimum_power():
    with pytest.raises(ValidationError):
        PowerConstraint(
            name="Invalid minimum power",
            min_power_kw=-1,
            max_power_kw=7.4,
        )