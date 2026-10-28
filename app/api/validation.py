"""Define reusable input validation and normalization rules for names and time zones."""

from typing import Annotated
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import AfterValidator, Field


def normalize_name(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("Name must not be blank")
    return value


def validate_timezone(value: str) -> str:
    value = value.strip()
    try:
        ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError):
        raise ValueError("Invalid time zone identifier")
    return value


NameField = Annotated[
    str,
    Field(min_length=1, max_length=100),
    AfterValidator(normalize_name),
]

TimezoneField = Annotated[
    str,
    Field(min_length=1, max_length=100),
    AfterValidator(validate_timezone),
]
