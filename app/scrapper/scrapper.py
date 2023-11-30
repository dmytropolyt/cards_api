from typing import Union
import random

import requests


class Scrapper:
    """
    Class for interacting with SampleAPI to get Playstation games.
    """
    url = 'https://api.sampleapis.com/playstation/games'

    def get_all_games(self) -> dict:
        return requests.get(self.url).json()

    def _get_by_parameter(
            self, param: Union[str, list[str]]
    ) -> tuple[dict, Union[set, str]]:
        data = self.get_all_games()
        param = set(param) if isinstance(param, list) else param

        return (data, param)

    def get_random_game(self) -> dict:
        games = self.get_all_games()

        return random.choice(games)

    def get_by_name(self, names: Union[str, list[str]]) -> list[dict]:
        """
        Can accept string ot list.
        And it will return a list with games with specified names.
        """
        games, names = self._get_by_parameter(names)
        key = 'name'

        return [game for game in games if game.get(key) in names]

    def get_by_genres(self, genres: Union[str, list[str]]) -> list[dict]:
        """
        Can accept string ot list.
        And it will return a list with games with specified genres.
        """
        games, genres = self._get_by_parameter(genres)
        key = 'genre'

        return [game for game in games for genre in game.get(key) if genre in genres]

    def get_by_developers(self, developers: Union[str, list[str]]) -> list[dict]:
        """
        Can accept string ot list.
        And it will return a list with games with specified developers.
        """
        games, developers = self._get_by_parameter(developers)
        key = 'developers'

        return [
            game for game in games
            for developer in game.get(key) if developer in developers
        ]

    def get_by_publishers(self, publishers: Union[str, list[str]]) -> list[dict]:
        """
        Can accept string ot list.
        And it will return a list with games with specified publishers.
        """
        games, publishers = self._get_by_parameter(publishers)
        key = 'publishers'

        return [
            game for game in games
            for publisher in game.get(key) if publisher in publishers
        ]

    def get_by_release(self, release: Union[str, list[str]]) -> list[dict]:
        """
        Can accept string ot list.
        And it will return a list with games with specified release dates.
        """
        games, releases = self._get_by_parameter(release)
        key = 'releaseDates'

        return [
            game for game in games
            for release in game.get(key).values() if release in releases
        ]
