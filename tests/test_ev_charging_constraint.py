
import pytest
from pydantic import ValidationError

from app.domain.constraints import EVChargingConstraint


def test_ev_charging_constraint_accepts_valid_power():
    constraint = EVChargingConstraint(
        name="EV charging limit",
        max_charge_kw=7.4,
    )

    assert constraint.max_charge_kw == 7.4


@pytest.mark.parametrize("max_charge_kw", [0, -1, -7.4])
def test_ev_charging_constraint_rejects_nonpositive_power(
    max_charge_kw,
):
    with pytest.raises(ValidationError):
        EVChargingConstraint(
            name="Invalid EV charging limit",
            max_charge_kw=max_charge_kw,
        )