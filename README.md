# iHeartInternetRadio

Command-line interface for gathering and processing internet radio streams.

## CLI

The `cli` module is intended to be run by invocation as a shell command shown by the help screen below:

```
Usage: iheartir [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose  Increases the verbosity of the output up to three (3) times.
                 By default, everything except errors is suppressed.
  --help         Show this message and exit.

Commands:
  info       Gets information about the radio station from the provided url
  providers  Lists the available search providers for radio streams
  search     Performs a search for matching radio station from all 
  stream     Gets the best stream url from the provided url


Usage: iheartir info URL

  Gets information about the radio station from the provided url


Usage: iheartir providers

  Lists the available search providers for radio streams


Usage: iheartir search [OPTIONS] SEARCH_STRING

  Performs a search for matching radio station from all providers

Options:
  -l, --limit INTEGER RANGE  Sets the maximum number of results returned by
                             each provider  [x>=1]


Usage: iheartir stream [OPTIONS] URL

  Gets the best stream url from the provided url

Options:
  -t, --type  If set, also shows the type of the returned stream
```

### Examples

#### Searching for up to two stations
```bash
$ iheartir search --limit 2 "radio 1045"`
```

```
ALT 104.5
  Philly's Alternative Rock
  WRFF-FM
  Genre: Alternative
  Frequency: 104.5
  URL: https://www.iheart.com/live/3401
  Image URL: https://i.iheart.com/v3/re/new_assets/5ecd457d5466175faca5bcf8
  Score: 0.07070309
  Provider: iheartradio

104.5 WXLO
  New England’s Best Variety
  WXLO-FM
  Genre: Mix & Variety
  Frequency: 104.5
  URL: https://www.iheart.com/live/5380
  Image URL: https://i.iheart.com/v3/re/new_assets/5bd76b42655fe92a11715487
  Score: 0.055565815
  Provider: iheartradio
```
#### Getting the information for the first station
```bash
$ iheartir info "https://www.iheart.com/live/3401"
```

```
ALT 104.5
  Philly's Alternative Rock
  WRFF-FM
  Genre: Alternative
  Frequency: 104.5
  URL: https://www.iheart.com/live/alt-1045-3401/
  Image URL: https://i.iheart.com/v3/re/new_assets/5ecd457d5466175faca5bcf8
  Streams:
    hls_stream: http://stream.revma.ihrhls.com/zc3401/hls.m3u8
    shoutcast_stream: http://stream.revma.ihrhls.com/zc3401
    secure_hls_stream: https://stream.revma.ihrhls.com/zc3401/hls.m3u8
    secure_shoutcast_stream: https://stream.revma.ihrhls.com/zc3401
  Score: 0
  Provider: iheartradio
```

#### Retrieving the best stream from the second station
```bash
$ iheartir stream -t "https://www.iheart.com/live/5380"
```

```
secure_pls_stream: https://playerservices.streamtheworld.com/pls/WXLOFMAAC.pls
```

### Debugging

While `iheartir` is designed to safely and silently handle most common issues, sometimes seeing more complex messages is useful.

To see more detailed feedback when using the cli, utilize the `-v` or `--verbose` option. `iheartir -v` will print non-fatal warning messages along with standard output, `iheartir -vv` will print basic debugging information along with non-fatal warnings and standard output, and `iheartir -vvv` will print a *huge* amount of debugging information along with all the other outputs. Using `-v` in scripts is not reccomended, as the outputs generated depend highly on the logging implementations of other packages as well as those in `iheartir`.

## API

The `api` module provides access to the functions underlying the `cli` module and can be used to implement custom logic using the same repository of stream providers. These functions primarily output a `Station` object with the attributes and defaults listed below:

```python
provider: str
station_id: str
name: str
call_letters: str = ""
description: str = ""
genre: str = ""
frequency: str = ""
url: str = ""
image: str = ""
streams: dict = {}
score: float = 0
```
The following is a rundown of each function in the api:

```python
import iheartir
import iheartir.api as api

# Displays all station providers registered and successfully loaded at import
print(iheartir.PROVIDERS)

# Attempts to load all registered plugins and displays the successfully loaded ones 
print(api.get_providers())

# Perform a search for the top 2 matching radio stations and returns a list of Station objects
station_results = api.search_stations("radio 1045", limit=2)
print(station_results[0])

# Returns a Station object representing the station from the provided url
station2 = api.get_station_info(station_results[1].url)
print(station2)

# Updates the Station object from the search results to full information
station = api.update_station_info(station)
print(station_results)

# Returns a tuple with the best available stream from the Station object and the format of that stream
best_station = api.get_best_stream(station)
```

## Implementing Custom Providers

To be successfully loaded, a station provider plugin must implement the `StationProvider` protocol as defined below:

```python
class StationProvider(_typing.Protocol):
    """Protocol representing a provider of internet radio stations compatible with this parser"""

    def get_id(self) -> str:
        """Should return a unique lowercase string identifying the provider"""
        pass

    def get_name(self) -> str:
        """Should return the name of the provider"""
        pass

    def get_base_url() -> str:
        """Should return the base url for the provider"""
        pass

    def search(self, search_string: str, limit: int) -> _typing.List[Station]:
        """Searches the provider for stations matching the search text"""
        pass

    def get(self, station_id: str) -> Station:
        """Returns a Station object representing a station from the provider"""
        pass

    def match(self, url: str) -> bool:
        """Determines if the given url is from the provider"""
        pass
```
In addition, the class that implements this protocol must be declared as an entry point in `pyproject.toml` or similarly declared like so:

```toml
[tool.poetry.plugins."iheartir.providers"]
MyNewProviderClass = "path.to.class:MyNewProviderClass"
```

## To-Do
- [ ] Test on `test.pypi.org`
- [ ] Upload to `pypi.org`
- [ ] Add more thorough unit testing
- [ ] RhythmBox plugin (this was the original use-case)
- [ ] Add additional default providers