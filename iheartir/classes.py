import typing as _typing

__all__ = ["Station", "StationProvider"]


class Station:
    '''Class representing a specific internet radio station with common attributes'''

    __slots__ = (
        "provider",
        "station_id",
        "name",
        "call_letters",
        "description",
        "genre",
        "frequency",
        "url",
        "image",
        "streams",
        "score",
    )

    def __init__(
        self,
        provider: str,
        station_id: str,
        name: str,
        call_letters: str = "",
        description: str = "",
        genre: str = "",
        frequency: str = "",
        url: str = "",
        image: str = "",
        streams: dict = {},
        score: float = 0,
    ):
        self.provider = provider
        self.station_id = station_id
        self.name = name
        self.call_letters = call_letters
        self.description = description
        self.genre = genre
        self.frequency = frequency
        self.url = url
        self.image = image
        self.streams = streams
        self.score = score

    def __repr__(self):
        streams = "\n    ".join([f"{k}: {v}" for k, v in self.streams.items()])
        return f"{self.name}\n  {self.description}\n  {self.call_letters}\n  Genre: {self.genre}\n  Frequency: {self.frequency}\n  URL: {self.url}\n  Image URL: {self.image}\n  Streams:\n    {streams}\n  Score: {self.score}\n  Provider: {self.provider}\n"

    def __eq__(self, other: _typing.Any) -> bool:
        return type(self) == type(other) and self.provider == other.provider and self.station_id == other.station_id and self.name == other.name and self.call_letters == other.call_letters and self.description == other.description
    


@_typing.runtime_checkable
class StationProvider(_typing.Protocol):
    '''Protocol representing a provider of internet radio stations compatible with this parser'''

    @_typing.abstractmethod
    def get_id(self) -> str:
        '''Should return a unique lowercase string identifying the provider'''
        pass

    @_typing.abstractmethod
    def get_name(self) -> str:
        '''Should return the name of the provider'''
        pass

    @_typing.abstractmethod
    def get_base_url() -> str:
        '''Should return the base url for the provider'''
        pass

    @_typing.abstractmethod
    def search(self, search_string: str, limit: int) -> _typing.List[Station]:
        '''Searches the provider for stations matching the search text'''
        pass

    @_typing.abstractmethod
    def get(self, station_id: str) -> Station:
        '''Returns a Station object representing a station from the provider'''
        pass

    @_typing.abstractmethod
    def match(self, url: str) -> bool:
        '''Determines if the given url is from the provider'''
        pass
