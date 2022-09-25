from .api import get_providers
from .api import search_stations
from .api import get_station_info
from .classes import Station
from .classes import StationProvider
import logging

__all__ = [
    "PROVIDERS",
    "search_stations",
    "get_station_info",
    "Station",
    "StationProvider",
]

PROVIDERS = get_providers()

# Setup a basic
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(name)-12s:%(levelname)-8s:%(message)s",
    filename="/tmp/iheartir.log",
    filemode="w",
)
