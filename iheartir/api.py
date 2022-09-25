import iheartir as _iheartir
import iheartir.classes as _classes
import typing as _typing
import logging as _logging
from importlib.metadata import entry_points as _entry_points

__all__ = ["get_providers", "search_stations", "get_station_info"]


def get_providers():
    '''Loads all entry points registered as a provider, confirms that it matches the protocol, and loads it'''
    discovered_plugins = _entry_points().get("iheartir.providers")
    providers = []
    for entry_point in discovered_plugins:
        provider = entry_point.load()
        if isinstance(provider, _classes.StationProvider):
            providers.append(provider)
        else:
            _logging.warning(
                "Found plugin %s, but skipped it as it was not a valid provider"
                % provider
            )
    return providers


def search_stations(search_string: str, limit: int = 10) -> _typing.List[_classes.Station]:
    '''Performs a search for matching radio station on all stream providers'''
    _logging.debug("Querying providers for best results")
    stations = []
    for provider in get_providers():
        stations += provider.search(search_string, limit)
    if len(stations) == 0:
        _logging.warn("No matching stations returned")
    stations.sort(key=lambda station: station.score, reverse=True)
    return stations


def get_station_info(url: str) -> _classes.Station:
    '''Returns information about the radio station from the provided url'''
    _logging.debug("Beginning search for matching provider")
    for provider in _iheartir.PROVIDERS:
        if provider.match(url):
            _logging.info("Found matching provider: %s" % provider)
            results = provider.get(url)
            break
    else:
        _logging.warn("Unable to find matching provider")
    return results