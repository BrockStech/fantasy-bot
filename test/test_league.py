from src.league import League
import unittest

default_sleeper_league = 289646328504385536


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.league = League(default_sleeper_league)
        cls.user = cls.league._users[0]
        cls.roster = cls.league._rosters[0]
        cls.league.current_week = 10
        cls.league.predicted_points = cls.league.create_predicted_points_dictionary()
        cls.league.median = cls.league.calculate_league_median()

    def test_get_user_id(self):
        user_id = self.league.get_user_id(self.user)
        self.assertEqual(user_id, '457511950237696')

    def test_get_team_name(self):
        team_name = self.league.get_team_name(self.user)
        self.assertEqual(team_name, 'Giant Dolphins')

    def test_team_name_dict(self):
        roster_id = self.league.get_roster_id(self.roster)
        self.assertEqual(self.league.team_name_dict[roster_id], 'Kamara is the new DJ')

    def test_playoff_bracket_prediction(self):
        self.assertEqual(self.league.winners_bracket_prediction(), [])

    def test_faab_remaining(self):
        self.assertEqual(self.league.faab_remaining()[5], (0, '🔥Gordon x Gordon 🔥'))

    def test_matchup_prediction(self):
        for matchup in self.league.matchup_prediction().values():
            if matchup[0] == 'Kamara is the new DJ':
                self.assertEqual(matchup[2], 'Bless em 🙏🇨🇱')
                self.assertTrue(matchup[1] < matchup[3])

    def test_weekly_matchup(self):
        for matchup in self.league.matchup_prediction().values():
            if matchup[0] == 7:
                self.assertEqual(self.league.weekly_matchup(),
                                 [7, 159.4600067138672, 12, 145.9199981689453])

    def test_win_probability(self):
        self.assertTrue(.60 < self.league.get_win_probability(1, 2) < .66)

    def test_league_median(self):
        self.assertTrue(130 < self.league.median < 133)

    def test_predicted_win_total(self):
        team_old = None
        for team in self.league.predicted_win_total():
            if team_old is not None:
                self.assertTrue(team_old[1] >= team[1])
            else:
                self.assertEqual(team[0], 6)
                self.assertTrue((13 < team[1] < 14))
            team_old = team

    def test_standings(self):
        team_old = None
        for team in self.league.standings():
            if team_old is not None:
                self.assertTrue(int(team_old[1]) >= int(team[1]))
            else:
                self.assertEqual(team[0], 'Bless em 🙏🇨🇱')
                self.assertEqual(team[1], '11')
                self.assertEqual(team[2], '2')
                self.assertEqual(team[3], '1899')
                self.assertEqual(team[4], '2161')
            team_old = team
