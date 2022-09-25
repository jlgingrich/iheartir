from click.testing import CliRunner
from iheartir.cli import cli

def test_providers():
    '''Confirms that the CLI providers function works properly'''
    runner = CliRunner()
    result = runner.invoke(cli, ['providers'])
    assert result.exit_code == 0

def test_info():
    '''Confirms that the CLI info function works properly'''
    station_url = "https://www.iheart.com/live/alt-1045-3401/"
    runner = CliRunner()
    result = runner.invoke(cli, ['info', station_url])
    assert result.exit_code == 0

def test_search():
    '''Confirms that the CLI info function works properly'''
    search_string = "alt 1045"
    runner = CliRunner()
    result = runner.invoke(cli, ['search', search_string])
    assert result.exit_code == 0
