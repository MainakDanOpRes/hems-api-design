"""Define application-level exceptions for missing homes and devices."""

class HomeNotFoundError(Exception):
    """Raised when a requested home does not exist."""


class DeviceNotFoundError(Exception):
    """Raised when a requested device does not exist."""