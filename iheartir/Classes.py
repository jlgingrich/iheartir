from typing import runtime_checkable, Protocol, abstractmethod, List

class Station():
    """Class representing a specific internet radio station with common attributes"""

    def __init__(self,
                 station_id: str,
                 name: str,
                 call_letters: str = "",
                 description: str = "",
                 genre: str = "",
                 frequency: str = "",
                 url: str = "",
                 image: str = "",
                 streams: dict = {}):
        self.station_id = station_id
        self.name = name
        self.call_letters = call_letters
        self.description = description
        self.genre = genre
        self.frequency = frequency
        self.url = url
        self.image = image
        self.streams = streams

    def __repr__(self):
        return "\n".join(["%-30s%s" % (str(k), str(v)) for k, v in self.__dict__.items() if k != "streams"]) + "\nstreams:\n  " + "\n  ".join(["%-30s%s" % (str(k), v) for k, v in self.streams.items()])

    def __str__(self):
        return "\n".join([str(v) for k, v in self.__dict__.items() if k in {"name", "description", "station_url"}]) + "\n\nStreams:\n  " + "\n  ".join(["%-30s%s" % (str(k), v) for k, v in self.streams.items()])


@runtime_checkable
class StationProvider(Protocol):
    """Protocol representing a provider of internet radio stations"""
    name: str
    base_url: str

    @abstractmethod
    def search(self, search_string: str, l: int) -> List[Station]:
        """Searches the provider for stations matching the search text"""
        pass
    
    @abstractmethod
    def get(self, station_id: str) -> Station:
        """Returns a Station object representing a station from the provider"""
        pass

    @abstractmethod
    def match(self, url: str) -> bool:
        """Determines if the given url is from the provider"""
        pass
