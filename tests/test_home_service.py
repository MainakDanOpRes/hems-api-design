"""Test home-service behavior, including successful retrieval and missing-home errors."""

import pytest

from app.domain.home import Home
from app.repositories.memory import InMemoryHomeRepository
from app.services.exceptions import HomeNotFoundError
from app.services.home_service import HomeService, HomeRegistrationData


def test_get_home_returns_existing_home():
    repository = InMemoryHomeRepository()
    service = HomeService(home_repository=repository)

    home = Home(
        id="home-1",
        name="Test Home",
        timezone="Europe/Paris",
        max_import_kw=12.0,
        max_export_kw=6.0,
    )
    repository.save(home)

    result = service.get_home("home-1")

    assert result == home


def test_get_home_raises_error_when_home_does_not_exist():
    repository = InMemoryHomeRepository()
    service = HomeService(home_repository=repository)

    with pytest.raises(HomeNotFoundError, match="home-404"):
        service.get_home("home-404")
