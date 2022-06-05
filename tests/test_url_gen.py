from datetime import *
from URL_Manager.URL_Gen import UrlGenerator

def test_get_source():
    generator = UrlGenerator()
    target_url = 'https://www.reuters.com/technology/exclusive-ukraine-halts-half-worlds-neon-output-chips-clouding-outlook-2022-03-11/'
    response = generator.get_source(target_url)
    assert response.status_code == 200

def test_google_search_date():
    generator = UrlGenerator()
    day = date(2022, 1, 1)
    target_url = 'https://www.google.com/search?q=TSMC&tbs='
    search_time = generator.get_google_search_date(day)
    response = generator.get_source(target_url + search_time)
    assert response.status_code == 200

def test_parser():
    generator = UrlGenerator()
    day = date(2022, 1, 1)
    target_url = 'https://www.google.com/search?q=TSMC&tbm=nws&tbs='
    search_time = generator.get_google_search_date(day)
    response = generator.get_source(target_url + search_time)
    links = generator.parse_googleResults(response)
    assert len(links) > 0

