from src.formatter import Formatter
from src.league import League
import unittest
from unittest.mock import patch


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.formatter = Formatter()
        cls.formatter.league = League()
        cls.mock_standings = patch.object(
            cls.formatter.league, 'standings', return_value=[("Test Team", "13", "9", "1,304", "1,890")])
        cls.mock_matchup = patch.object(
            cls.formatter.league, 'matchup_prediction', return_value={1: ["Team 1", 65.55, "Team 2", 34.45],
                                                                      2: ["Team 3", 21.19, "Team 4", 78.81]})
        cls.mock_faab = patch.object(
            cls.formatter.league, 'faab_remaining', return_value=[(345, 'Test Team'), (292, 'Team 2')])

        cls.mock_waiver_type = patch.object(
            cls.formatter.league, 'get_waiver_type', return_value=2)

    def test_format_matchup(self):
        with self.mock_matchup:
            self.assertEqual(self.formatter.matchup(),
                             "Week " + str(self.formatter.current_week) +
                             " Matchups:\n\nTeam 1 (65.55%)\nTeam 2 (34.45%)\n\n"
                             "Team 3 (21.19%)\nTeam 4 (78.81%)\n\n")

    def test_format_standings(self):
        with self.mock_standings:
            self.assertEqual(self.formatter.standings(), "Standings:\n\nTest Team:\n\tRecord: 13-9\n\t"
                                                         "Points Scored: 1,304\n\tBest Ball: 1,890\n")

    def test_format_faab(self):
        with self.mock_waiver_type:
            with self.mock_faab:
                self.assertEqual(self.formatter.faab(), "Remaining FAAB:\n\nTest Team (345)\n"
                                                        "Team 2 (292)\n")
