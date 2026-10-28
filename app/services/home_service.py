from typing import Protocol

from app.domain.home import Home
from uuid import uuid4


class HomeRepository(Protocol):
    def save(self, home: Home) -> Home:
        ...


class HomeRegistrationData:
    def __init__(
        self,
        name: str,
        timezone: str,
        max_import_kw: float,
        max_export_kw: float,
    ) -> None:
        self.name = name
        self.timezone = timezone
        self.max_import_kw = max_import_kw
        self.max_export_kw = max_export_kw


class HomeService:
    def __init__(self, home_repository: HomeRepository) -> None:
        self.home_repository = home_repository

    def register_home(self, data: HomeRegistrationData) -> Home:
        home = Home(
            id=str(uuid4()),
            name=data.name,
            timezone=data.timezone,
            max_import_kw=data.max_import_kw,
            max_export_kw=data.max_export_kw,
        )
        return self.home_repository.save(home)