from iheartir import PROVIDERS as _PROVIDERS
import iheartir.api as _api
import click as _click
import logging as _logging

__all__ = []


@_click.group()
@_click.option(
    "-v",
    "--verbose",
    count=True,
    help="Increases the verbosity of the output up to three (3) times. By default, everything except errors is suppressed.",
)
def cli(verbose):

    # Sets up a console handler in addition to the existing logfile handler
    console = _logging.StreamHandler()
    formatter = _logging.Formatter("%(name)s:%(levelname)s %(message)s")
    console.setFormatter(formatter)

    # Default logging level for console is error, since this is for a command-line script and it should silently fail
    console.setLevel(_logging.ERROR)
    if verbose:
        if verbose >= 3:
            level = _logging.DEBUG
        elif verbose == 2:
            level = _logging.INFO
        elif verbose == 1:
            level = _logging.WARNING
        console.setLevel(level)
    _logging.getLogger("").addHandler(console)
    # From here, control passes to the called command


@cli.command()
@_click.argument("search_string", nargs=1)
@_click.option(
    "-l",
    "--limit",
    type=_click.IntRange(0, clamp=True),
    default=10,
    help="Sets the maximum number of results returned by each provider",
)
def search(search_string, limit):
    """Performs a search for matching radio station from all providers"""
    results = _api.search_stations(search_string, limit)
    if len(results) > 10:
        _click.echo_via_pager(results)
    else:
        for result in results:
            _click.echo(result)


@cli.command()
@_click.argument("url", nargs=1)
def info(url):
    """Gets information about the radio station from the provided url"""
    _click.echo(_api.get_station_info(url))


@cli.command()
def providers():
    """Lists the available search providers for radio streams"""
    [_click.echo(provider.get_name()) for provider in _PROVIDERS]
