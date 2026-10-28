
import pytest
from pydantic import ValidationError

from app.domain.home import Home


def test_home_rejects_infinite_import_limit():
    with pytest.raises(ValidationError):
        Home(
            id="home-1",
            name="Test Home",
            timezone="Europe/Paris",
            max_import_kw=float("inf"),
            max_export_kw=6.0,
        )


def test_home_rejects_infinite_export_limit():
    with pytest.raises(ValidationError):
        Home(
            id="home-2",
            name="Test Home",
            timezone="Europe/Paris",
            max_import_kw=12.0,
            max_export_kw=float("inf"),
        )
