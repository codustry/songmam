# type: ignore[attr-defined]
"""a facebook messenger hypermodern python library based on fastapi. """


from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from .api import MessengerApi
from .webhook import WebhookHandler
