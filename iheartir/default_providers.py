from iheartir.Classes import StationProvider, Station
import typing
import bs4
import json
import requests
import logging
import re

class _IHeartRadioProvider(object):
    """Default StationProvider implementation for iHeart Radio"""
    def __init__(self):
        self.name = "iHeart Radio (Built-in)"
        self.base_url = "https://www.iheart.com/live/"

    def __repr__(self):
        return "%s Provider" % self.name

    def get(self, station_url: str) -> Station:
        """Returns a Station object containing all information for the selected station"""
        response = self._get_station_response(station_url)
        return self._process_station_response(response)

    def _get_station_response(self, station_url: str) -> requests.models.Response:
        """Requests the to the backend iHeart Radio Search API."""
        response = requests.get(url=station_url)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            logging.error("HTTPError when trying to get " + station_url)
        logging.info("Status code %s" % str(response.status_code))
        return response

    def _process_station_response(self, response: requests.models.Response) -> Station:
        """Extracts and converts the initial first."""
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        stations = json.loads(soup.find(id="initialState").getText())[
            "live"]["stations"]
        station_data = stations[list(stations.keys())[0]]
        return self._as_station(station_data)

    def _as_station(self, item: typing.Dict):
        """Attempts to create a Station protocol-compatible object from the given list"""
        try:
            station = Station(
                station_id = str(item["id"]),
                name = item["name"],
                call_letters = item["callLetters"],
                description = item["description"],
                genre = item["genres"][0]["name"],
                frequency = item["freq"],
                url = self.base_url + str(item["id"]),
                image = item["logo"],
                streams = item["streams"]
            )
        except KeyError:
            raise ValueError("dict cannot be coerced to station")
        return station

    def search(self, search_string: str, max_rows: int = 10) -> typing.List[Station]:
        """Returns a list of Station urls with names or descriptions matching the search string"""
        response = self._get_search_api_response(search_string, max_rows=max_rows)
        return self._process_search_api_response(response)

    def _get_search_api_response(
        self,
        search_string: str,
        url: str = "https://us.api.iheart.com/api/v3/search/all",
        start_index: int = 0,
        max_rows: int = 10,
        include_stations: bool = True,
        include_albums: bool = False,
        include_artists: bool = False,
        include_bundles: bool = False,
        include_playlists: bool = False,
        include_podcasts: bool = False,
        include_tracks: bool = False
    ) -> requests.models.Response:
        """Wrapped request to the backend iHeart Radio Search API."""
        params = {
            "keywords": search_string,
            "startIndex": start_index,
            "maxRows": max_rows,
            "station": include_stations,
            "albums": include_albums,
            "artist": include_artists,
            "bundle": include_bundles,
            "playlist": include_playlists,
            "podcast": include_podcasts,
            "track": include_tracks
        }
        return requests.get(url=url.lower(), params=params)

    def _process_search_api_response(self, response: requests.models.Response) -> typing.List[str]:
        stations = json.loads(response.content)["results"]["stations"]
        return [self.get(self.base_url + str(station["id"])) for station in stations]

    def match(self, url: str) -> bool:
        return bool(re.search(r"^(?:https?://)?(?:\w{3}\.)?iheart.com/live/(?:[a-z0-9]+-)*[0-9]{4}/?$", url))

IHeartRadioProvider = _IHeartRadioProvider()