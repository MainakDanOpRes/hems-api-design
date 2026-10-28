"""Test device availability constraints and their validation rules."""
from datetime import datetime

import pytest
from pydantic import ValidationError

from app.domain.constraints import AvailabilityConstraint


def test_availability_constraint_accepts_valid_window():
    start = datetime(2026, 10, 9, 18, 0)
    end = datetime(2026, 10, 10, 7, 0)

    constraint = AvailabilityConstraint(
        name="EV availability",
        available_from=start,
        available_until=end,
    )

    assert constraint.available_from == start
    assert constraint.available_until == end

def test_availability_constraint_rejects_reversed_window():
    with pytest.raises(ValidationError) as exc_info:
        AvailabilityConstraint(
            name="Invalid availability",
            available_from=datetime(2026, 10, 10, 7, 0),
            available_until=datetime(2026, 10, 9, 18, 0),
        )

    assert "available_from" in str(exc_info.value)

def test_availability_constraint_accepts_equal_timestamps():
    timestamp = datetime(2026, 10, 9, 18, 0)

    constraint = AvailabilityConstraint(
        name="Instant availability",
        available_from=timestamp,
        available_until=timestamp,
    )

    assert constraint.available_from == constraint.available_until