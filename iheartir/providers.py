import iheartir.classes as _classes
import typing as _typing
import logging as _logging
import json as _json
import requests as _requests
import re as _re
import lxml.etree as _etree
import sys as _sys

__all__ = ["IHeartRadioProvider"]


class IHeartRadioProvider(object):
    """Default StationProvider implementation for iHeart Radio"""

    def __init__(self):
        self._id = "iheartradio"
        self._name = "iHeart Radio (Built-in)"
        self._base_url = "https://www.iheart.com"

    def __repr__(self):
        return "%s Provider" % self._name

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_base_url(self):
        return self._base_url

    def get(self, station_url: str) -> _classes.Station:
        """Returns a Station object containing all information for the selected station"""
        try:
            response = _requests.get(url=station_url)
            response.raise_for_status()
        except _requests.HTTPError:
            _logging.error("HTTPError when trying to get " + station_url)
            _sys.exit(0)
        except _requests.exceptions.ConnectionError:
            _logging.error("ConnectionError when trying to get " + station_url)
            _sys.exit(0)
        _logging.info("Status code %s" % str(response.status_code))
        html = _etree.HTML(response.content)
        target = html.xpath(r"//script[@id='initialState']")[0].text
        stations = _json.loads(target)["live"]["stations"]
        station_data = stations[list(stations.keys())[0]]
        return _classes.Station(
            provider=self.get_id(),
            station_id=station_data["id"],
            name=station_data["name"],
            call_letters=station_data["callLetters"],
            description=station_data["description"],
            genre=station_data["genres"][0]["name"],
            frequency=station_data["freq"],
            url=self.get_base_url() + station_data["url"],
            image=station_data["logo"],
            streams=station_data["streams"],
            score=0,  # Defaults to 0 since its not relevant for an info request
        )

    def search(
        self,
        search_string: str,
        limit: int = 10,
        start_index: int = 0,
        url: str = "https://us.api.iheart.com/api/v3/search/all",
        include_stations: bool = True,
        include_albums: bool = False,
        include_artists: bool = False,
        include_bundles: bool = False,
        include_playlists: bool = False,
        include_podcasts: bool = False,
        include_tracks: bool = False,
    ) -> _typing.List[_classes.Station]:
        """Wrapped request to the backend iHeart Radio Search API that loads the json result into Station objects."""
        params = {
            "keywords": search_string,
            "startIndex": start_index,
            "maxRows": limit,
            "station": include_stations,
            "albums": include_albums,
            "artist": include_artists,
            "bundle": include_bundles,
            "playlist": include_playlists,
            "podcast": include_podcasts,
            "track": include_tracks,
        }
        response = _requests.get(url=url.lower(), params=params)
        results = _json.loads(response.content)["results"]["stations"]
        return [
            _classes.Station(
                provider=self.get_id(),
                station_id=result["id"],
                name=result["name"],
                call_letters=result["callLetters"],
                description=result["description"],
                genre=result["genre"],
                frequency=result["frequency"],
                url=f"{self.get_base_url()}/live/{str(result['id'])}",
                image=result["imageUrl"],
                # streams=NULL
                score=result["score"],
            )
            for result in results
        ]

    def match(self, url: str) -> bool:
        return bool(
            _re.search(
                r"^(?:https?://)?(?:\w{3}\.)?iheart.com/live/(?:[a-z0-9]+-)*[0-9]{4}/?$",
                url,
            )
        )
