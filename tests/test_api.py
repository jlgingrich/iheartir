import iheartir

expected_result = iheartir.classes.Station(
    provider=iheartir.PROVIDERS[0].get_id(),
    station_id=3401,
    name="ALT 104.5",
    description="Philly's Alternative Rock",
    call_letters="WRFF-FM",
    frequency="104.5",
    image="https://i.iheart.com/v3/re/new_assets/5ecd457d5466175faca5bcf8",
    score=0,
    url="https://www.iheart.com/live/alt-1045-3401/",
    genre="Alternative",
)

def test_get():
    """Confirms that the website is avaliable, the html and json parsers are still functioning, and the get function works as expected"""
    station_url = "https://www.iheart.com/live/alt-1045-3401/"
    result = iheartir.api.get_station_info(station_url)
    assert result == expected_result


def test_search():
    """Confirms that the search api is avaliable, the json parser is still functioning, and the search function works as expected"""
    search_string = "alt 1045"
    result = iheartir.api.search_stations(search_string, limit=1)[0]
    assert result == expected_result
