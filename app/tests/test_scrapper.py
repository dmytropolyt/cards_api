import pytest

import requests

from scrapper import scrapper


class TestScrapper:
    """Tests for Scrapper."""
    url = 'https://api.sampleapis.com/playstation/games'
    scrapper = scrapper.Scrapper()

    def test_get_all_games(self):
        games = requests.get(self.url).json()

        scrapper_games = self.scrapper.get_all_games()
        assert len(games) == len(scrapper_games)
        assert games == scrapper_games

    @pytest.mark.parametrize(
        'key',
        ['name', 'genre', 'developers', 'publishers', 'releaseDates']
    )
    def test_get_random_game(self, key):
        game = self.scrapper.get_random_game()

        assert key in game.keys()

    @pytest.mark.parametrize(
        'name',
        ['Just Cause 4', ["100ft Robot Golf", "Aaero"]]
    )
    def test_get_by_name(self, name):
        result = self.scrapper.get_by_name(name)

        for game in result:
            assert game.get('name') in name

    @pytest.mark.parametrize(
        'genre',
        ['Shooter', ["Sports", "Hidden object"]]
    )
    def test_get_by_genres(self, genre):
        result = self.scrapper.get_by_genres(genre)

        for game in result:
            assert str(*game.get('genre')) in genre

    @pytest.mark.parametrize(
        'developers',
        ["Gloomywood", ["Sobaka Studio", "Bitmap Bureau"]]
    )
    def test_get_by_developers(self, developers):
        result = self.scrapper.get_by_developers(developers)

        for game in result:
            assert str(*game.get('developers')) in developers

    @pytest.mark.parametrize(
        'publishers',
        ["Bigben Interactive", ["Code Horizon", "QuByte Interactive"]]
    )
    def test_get_by_publishers(self, publishers):
        result = self.scrapper.get_by_publishers(publishers)

        for game in result:
            assert str(*game.get('publishers')) in publishers

    def test_get_by_release_single_date(self):
        release = "Jun 29, 2017"
        result = self.scrapper.get_by_release(release)

        for game in result:
            assert release in game.get('releaseDates').values()

    def test_get_by_release_multiple_dates(self):
        release = ["Apr 7, 2015", "Apr 11, 2017"]

        result = self.scrapper.get_by_release(release)

        for game in result:
            dates = game.get('releaseDates').values()
            assert any(date in release for date in dates)
