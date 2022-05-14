from .sleeper_api import SleeperApi
from statistics import mean, stdev
from collections import defaultdict
from datetime import timedelta
import datetime
import numpy as np


class League:
    def __init__(self, league_id=None):
        if league_id is not None:
            self.api = SleeperApi(league_id)
            self._league = self.api.get_league()
            self._users = self.api.get_users()
            self._rosters = self.api.get_rosters()
            self._matchups = self.get_seasonal_matchups()
            self.team_name_dict = self.map_roster_id_to_team_name()
            self.current_week = self.get_week()
            self.schedule = self.get_schedule()
            self.predicted_points = self.create_predicted_points_dictionary()
            self.median = self.calculate_league_median()

    @staticmethod
    def get_team_name(user):
        try:
            user_id = user["metadata"]["team_name"].strip()
        except KeyError:
            user_id = user["display_name"].strip()
        return user_id

    @staticmethod
    def get_user_id(user):
        return user["user_id"]

    @staticmethod
    def get_roster_id(roster):
        return roster["roster_id"]

    @staticmethod
    def get_owner_id(roster):
        return roster["owner_id"]

    @staticmethod
    def get_wins(roster):
        return roster["settings"]["wins"]

    @staticmethod
    def get_losses(roster):
        return roster["settings"]["losses"]

    @staticmethod
    def get_fpts(roster):
        return roster["settings"]["fpts"]

    @staticmethod
    def get_best_ball(roster):
        try:
            best_ball = roster["settings"]["ppts"]
        except KeyError:
            best_ball = 0
        return best_ball

    @staticmethod
    def get_faab(roster):
        return roster["settings"]["waiver_budget_used"]

    @staticmethod
    def get_points(matchup):
        return matchup["points"]

    @staticmethod
    def get_matchup_id(matchup):
        return matchup["matchup_id"]

    def get_sport(self):
        return self._league["sport"]

    def is_nfl(self):
        return bool(self.get_sport() == "nfl")

    def is_season_complete(self):
        return bool(self._league["status"] == "complete")

    def get_waiver_type(self):
        return int(self._league["settings"]["waiver_type"])

    def get_waiver_budget(self):
        return self._league["settings"]["waiver_budget"]

    def uses_league_median(self):
        return bool(self._league["settings"]["league_average_match"])

    def get_playoff_week_start(self):
        return self._league["settings"]["playoff_week_start"]

    def get_week(self):
        return self.api.get_state()["week"]

    def map_users_to_team_name(self):
        users_dict = {}
        for user in self._users:
            users_dict[self.get_user_id(user)] = self.get_team_name(user)
        return users_dict

    def map_roster_id_to_owner_id(self):
        roster_id_dict = {}
        for roster in self._rosters:
            roster_id_dict[self.get_roster_id(roster)] = self.get_owner_id(roster)
        return roster_id_dict

    def map_roster_id_to_team_name(self):
        users_dict = self.map_users_to_team_name()
        rosters_dict = self.map_roster_id_to_owner_id()
        team_name_dict = {}
        for roster in rosters_dict:
            team_name_dict[roster] = users_dict[rosters_dict[roster]]
        return team_name_dict

    def get_seasonal_matchups(self):
        season_matchup_dict = {}
        for week in range(1, self.get_playoff_week_start()):
            season_matchup_dict[week] = self.api.get_matchups(week)
        return season_matchup_dict

    def get_schedule(self):
        league_schedule_dict = {}
        for week in range(1, self.get_playoff_week_start()):
            for matchup in self._matchups[week]:
                roster_id, matchup_id = self.get_roster_id(matchup), self.get_matchup_id(matchup)
                if roster_id in league_schedule_dict.keys():
                    league_schedule_dict[roster_id].append(self.get_opponent(week, matchup_id, roster_id))
                else:
                    league_schedule_dict[roster_id] = [self.get_opponent(week, matchup_id, roster_id)]
        return league_schedule_dict

    def get_opponent(self, week, matchup_id, roster_id):
        matchup = self.get_matchup(week, matchup_id)
        return matchup[0] if roster_id is matchup[1] else matchup[1]

    def get_matchup(self, week, matchup_id):
        current_matchup = []
        for matchup in self._matchups[week]:
            if matchup_id is self.get_matchup_id(matchup):
                current_matchup.append(self.get_roster_id(matchup))
        return current_matchup

    def get_weekly_points_scored(self, roster_id):
        points_scored = []
        for week in range(1, self.current_week):
            if week <= len(self._matchups):
                for matchup in self._matchups[week]:
                    if roster_id is self.get_roster_id(matchup):
                        points_scored.append(self.get_points(matchup))
        return points_scored

    def get_average_points(self, roster_id):
        return mean(self.get_weekly_points_scored(roster_id))

    def get_standard_deviation(self, roster_id):
        return stdev(self.get_weekly_points_scored(roster_id))

    def generate_predicted_points(self, roster_id):
        std = self.get_standard_deviation(roster_id)
        avg = self.get_average_points(roster_id)
        return np.random.normal(avg, std, 10000)

    def create_predicted_points_dictionary(self):
        team_points_dictionary = {}
        for team in self.team_name_dict:
            team_points_dictionary[team] = self.generate_predicted_points(team)
        return team_points_dictionary

    def get_predicted_wins_from_matchups(self):
        predicted_wins = {}
        for team in self.team_name_dict:
            weekly_win_probability = []
            for opponent in self.schedule[team][self.current_week:]:
                weekly_win_probability.append(self.get_win_probability(team, opponent))
            predicted_wins[team] = sum(weekly_win_probability)
        return predicted_wins

    def get_win_probability(self, team, opponent):
        binary_win_loss = np.greater(self.predicted_points[team],
                                     self.predicted_points[opponent])
        loss, win = np.bincount(binary_win_loss)
        return self.calculateProbability(win, loss)

    def calculate_league_median(self):
        return np.median(list(self.predicted_points.values()))

    def get_predicted_wins_from_median(self, team):
        binary_above_below = np.greater(self.predicted_points[team], self.median)
        below, above = np.bincount(binary_above_below)
        return self.calculateProbability(above, below) * (self.get_playoff_week_start() - self.current_week)

    def predicted_win_total(self):
        team_playoff_points = {}
        predicted_wins = self.get_predicted_wins_from_matchups()
        for team in self.team_name_dict:
            predicted_playoff_points = predicted_wins[team] + self.get_wins(self._rosters[team - 1])
            if self.uses_league_median():
                predicted_playoff_points += self.get_predicted_wins_from_median(team)
            team_playoff_points[team] = predicted_playoff_points.round(2)
        return sorted(team_playoff_points.items(), key=lambda x: x[1], reverse=True)

    def standings(self):
        roster_standings_list = []
        for roster in self._rosters:
            roster_standings_list.append((self.get_wins(roster),
                                          self.get_losses(roster),
                                          self.get_fpts(roster),
                                          self.team_name_dict[self.get_roster_id(roster)],
                                          self.get_best_ball(roster)))
        roster_standings_list.sort(reverse=True)
        clean_standings_list = []
        for item in roster_standings_list:
            clean_standings_list.append((item[3], str(item[0]), str(item[1]), str(item[2]), str(item[4])))
        return clean_standings_list

    def weekly_matchup(self):
        matchups_dict = {}
        if self.current_week <= len(self._matchups):
            for matchup in self._matchups[self.current_week]:
                matchup_id = self.get_matchup_id(matchup)
                roster_id = self.get_roster_id(matchup)
                team_points = self.get_points(matchup)
                if matchup_id not in matchups_dict:
                    matchups_dict[matchup_id] = [roster_id, team_points]
                else:
                    matchups_dict[matchup_id].append(roster_id)
                    matchups_dict[matchup_id].append(team_points)
        return matchups_dict

    def matchup_prediction(self):
        matchup_dict = {}
        for matchup_id, teams in self.weekly_matchup().items():
            win_prob = self.get_win_probability(teams[0], teams[2])
            matchup_dict[matchup_id] = [self.team_name_dict[teams[0]], (win_prob * 100).round(2),
                                        self.team_name_dict[teams[2]], ((1 - win_prob) * 100).round(2)]
        return matchup_dict

    def faab_remaining(self):
        faab_remaining_list = []
        for roster in self._rosters:
            faab_remaining_list.append((self.get_waiver_budget() - self.get_faab(roster),
                                        self.team_name_dict[self.get_roster_id(roster)]))
        faab_remaining_list.sort(reverse=True)
        return faab_remaining_list

    def winners_bracket_prediction(self):
        return self.playoff_bracket_prediction(self.api.get_winners_bracket(), False)

    def losers_bracket_prediction(self):
        return self.playoff_bracket_prediction(self.api.get_losers_bracket(), True)

    def playoff_bracket_prediction(self, bracket, is_losers_bracket):
        matchup_probability = defaultdict(list)
        champ_prob = defaultdict(int)
        for matchup in bracket:
            if matchup['w'] is None:
                if matchup['t1'] is not None and matchup['t2'] is not None:
                    team1 = matchup['t1']
                    team2 = matchup['t2']
                    win_prob = self.get_win_probability(team1, team2)
                    if is_losers_bracket: win_prob = 1 - win_prob
                    matchup_probability[matchup['m']].append([team1, win_prob, team2, 1 - win_prob])
                elif matchup['t1'] is not None and matchup['t2_from'] is not None:
                    team1 = matchup['t1']
                    sub_bracket = self.get_parent_matchup(matchup['t2_from'])
                    for parent_matchup in matchup_probability[sub_bracket]:
                        win_prob1 = self.get_win_probability(team1, parent_matchup[0])
                        win_prob2 = self.get_win_probability(team1, parent_matchup[2])
                        if is_losers_bracket:
                            win_prob1 = 1 - win_prob1
                            win_prob2 = 1 - win_prob2
                        matchup_probability[matchup['m']].append(
                            [team1, win_prob1 * parent_matchup[1] + win_prob2 * parent_matchup[3]])
                        matchup_probability[matchup['m']].append(
                            [parent_matchup[0], (1 - win_prob1) * parent_matchup[1]])
                        matchup_probability[matchup['m']].append(
                            [parent_matchup[2], (1 - win_prob2) * parent_matchup[3]])
                elif matchup['t1_from'] is not None and matchup['t2_from'] is not None:
                    sub_bracket1 = self.get_parent_matchup(matchup['t1_from'])
                    sub_bracket2 = self.get_parent_matchup(matchup['t2_from'])
                    if sub_bracket2 is not None and sub_bracket1 is not None:
                        for team in matchup_probability[sub_bracket2]:
                            for opponent in matchup_probability[sub_bracket1]:
                                win_prob = self.get_win_probability(team[0], opponent[0])
                                if is_losers_bracket: win_prob = 1 - win_prob
                                champ_prob[team[0]] += win_prob * opponent[1]
                            champ_prob[team[0]] *= team[1]
                        for team in matchup_probability[sub_bracket1]:
                            for opponent in matchup_probability[sub_bracket2]:
                                win_prob = self.get_win_probability(team[0], opponent[0])
                                if is_losers_bracket: win_prob = 1 - win_prob
                                champ_prob[team[0]] += win_prob * opponent[1]
                            champ_prob[team[0]] *= team[1]
        return sorted(champ_prob.items(), key=lambda x: x[1], reverse=True)

    @staticmethod
    def get_playoff_matchup(bracket, matchup_id):
        for matchup in bracket:
            if matchup['m'] == matchup_id:
                return matchup

    @staticmethod
    def get_parent_matchup(parent_matchup_dict):
        if 'w' in parent_matchup_dict.keys():
            for matchup in parent_matchup_dict.values():
                return matchup

    @staticmethod
    def calculateProbability(win, loss):
        return win / (loss + win)
