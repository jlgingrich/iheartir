from iheartir import get_providers
import click
import logging

@click.group()
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True)
def cli(verbose):
    if (verbose):
        level = logging.DEBUG
        logger = logging.getLogger()
        logger.setLevel(level)
        for handler in logger.handlers:
            handler.setLevel(level)


@cli.command()
@click.argument('search_string', nargs=1)
def search(search_string):
    '''Performs a search for matching radio station on all stream providers'''
    logging.debug("Querying providers for best results")
    results = []
    for provider in get_providers():
        results += provider.search(search_string)
    for station in results:
        click.echo("%s: %s" % (station.name, station.url))
    if len(results)==0:
        logging.warn("No matching stations returned")

@cli.command()
@click.argument('url', nargs=1)
def get(url):
    '''Gets information about the radio station from the provided url'''
    logging.debug("Beginning search for matching provider")
    for provider in get_providers():
        if (provider.match(url)):
            logging.info("Found matching provider: %s" % provider)
            click.echo(provider.get(url))
            break
    else:
        logging.warn("Unable to find matching provider")

@cli.command()
def providers():
    '''Lists the avaliable search providers for radio streams'''
    logging.info("Lmao this is some providers alright")
    for provider in get_providers():
        print(provider.name)