import unittest
from statistics import Statistics
from player import Player


class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]


class TestStatistics(unittest.TestCase):
    def setUp(self):
        # annetaan Statistics-luokan oliolle "stub"-luokan olio
        self.statistics = Statistics(
            PlayerReaderStub()
        )

    def test_search_returns_right_player(self):
        player = self.statistics.search('Kurri')
        self.assertEqual(player.goals, 37)

    def test_search_returns_none_if_player_doesnt_exist(self):
        player = self.statistics.search('Testi')
        self.assertEqual(player, None)

    def test_team_returns_list_of_players(self):
        response = self.statistics.team('EDM')
        self.assertEqual(response[0].name, 'Semenko')

    def test_top_return_right_order(self):
        response = self.statistics.top(1)
        points = response[0].goals + response[0].assists
        self.assertAlmostEqual(points, 35+89)
