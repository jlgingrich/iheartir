import iheartir
import iheartir.api
import click
import logging

__all__ = []


@click.group()
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Increases the verbosity of the output up to three (3) times. By default, everything except errors is suppressed.",
)
def cli(verbose):

    # Sets up a console handler in addition to the existing logfile handler
    console = logging.StreamHandler()
    formatter = logging.Formatter("%(name)s:%(levelname)s %(message)s")
    console.setFormatter(formatter)

    # Default logging level for console is error, since this is for a command-line script
    console.setLevel(logging.ERROR)
    if verbose:
        if verbose >= 3:
            level = logging.DEBUG
        elif verbose == 2:
            level = logging.INFO
        elif verbose == 1:
            level = logging.WARNING
        console.setLevel(level)
    logging.getLogger("").addHandler(console)
    # From here, control passes to the called command


@cli.command()
@click.argument("search_string", nargs=1)
@click.option(
    "-l",
    "--limit",
    type=click.IntRange(0, clamp=True),
    default = 10,
    help="Sets the maximum number of results returned by each provider",
)
def search(search_string, limit):
    '''Performs a search for matching radio station from all providers'''
    results = iheartir.api.search_stations(search_string, limit)
    if len(results)>10:
        click.echo_via_pager(results)
    else:
        for result in results:
            click.echo(result)
        

@cli.command()
@click.argument("url", nargs=1)
def info(url):
    '''Gets information about the radio station from the provided url'''
    click.echo(iheartir.api.get_station_info(url))


@cli.command()
def providers():
    '''Lists the available search providers for radio streams'''
    [click.echo(provider.get_name()) for provider in iheartir.PROVIDERS]
