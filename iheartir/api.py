import iheartir as _iheartir
import iheartir.classes as _classes
import typing as _typing
import logging as _logging
from importlib.metadata import entry_points as _entry_points

__all__ = ["get_providers", "search_stations", "get_station_info"]


def get_providers():
    """Loads all entry points registered as a provider, confirms that it matches the protocol, and loads it"""
    discovered_plugins = _entry_points().get("iheartir.providers")
    providers = []
    for entry_point in discovered_plugins:
        # Loads the plugin class, initializes it, and confirms it matches the protocol
        try:
            plugin =  entry_point.load()
            provider = plugin()
            if isinstance(provider, _classes.StationProvider):
                providers.append(provider)
            else:
                _logging.warning(
                    f"Found plugin {provider}, but skipped it as it was not a valid provider"
                )
        except SyntaxError as e:
            _logging.error(
                f"Failed to load plugin {entry_point.name} due to {e.msg}"
            )
    return providers


def search_stations(
    search_string: str, limit: int = 10
) -> _typing.List[_classes.Station]:
    """Performs a search for matching radio station on all stream providers"""
    _logging.debug("Querying providers for best results")
    stations = []
    for provider in get_providers():
        stations += provider.search(search_string, limit)
    if len(stations) == 0:
        _logging.warn("No matching stations returned")
    else:
        _logging.info(f"Found {len(stations)} matching stations")
        stations.sort(key=lambda station: station.score, reverse=True)
    return stations


def get_station_info(url: str) -> _classes.Station:
    """Returns information about the radio station from the provided url"""
    _logging.debug("Beginning search for matching provider")
    for provider in _iheartir.PROVIDERS:
        if provider.match(url):
            _logging.info("Found matching provider: %s" % provider)
            results = provider.get(url)
            break
    else:
        _logging.warn("Unable to find matching provider")
    return results


def update_station_info(station: _classes.Station) -> _classes.Station:
    """Updates the information about the station from its url"""
    return get_station_info(url=station.url)
