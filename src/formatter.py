from .league import League
from .user_input_handler import sleeper_league_id


class Formatter:
    def __init__(self):
        self.league = League(sleeper_league_id())

    def standings(self):
        print_standing = "Standings:\n\n"
        for team in self.league.standings():
            print_standing += str(team[0] + ":\n" + "\t" + "Record: " + team[1]
                                  + "-" + team[2] + "\n\tPoints Scored: " + team[3])
            if team[4] != '0':
                print_standing += str("\n\tBest Ball: " + team[4])
            print_standing += "\n"
        return print_standing

    def faab(self):
        print_faab = None
        if self.league.get_waiver_type() == 2:
            print_faab = "Remaining FAAB:\n\n"
            for team in self.league.faab_remaining():
                print_faab += team[1] + " (" + str(team[0]) + ")\n"
        return print_faab

    def predicted_playoff_standings(self):
        print_pps = "Projected Win Totals:\n\n"
        for team in self.league.predicted_win_total():
            print_pps += str(self.league.team_name_dict[team[0]]) + ": " + str(team[1]) + "\n"
        return print_pps

    def matchup(self):
        print_matchup = "Week " + str(self.league.current_week) + " Matchups:\n\n"
        for matchup in self.league.matchup_prediction().values():
            if self.league.current_week == 1:
                print_matchup += (matchup[0] + " vs " + matchup[2])
            else:
                print_matchup += (matchup[0] + " (" + str(matchup[1]) + "%)"
                                  + "\n" + matchup[2] + " (" + str(matchup[3]) + "%)\n\n")
        return print_matchup

    def scoreboard(self):
        print_standing = "Scoreboard:\n\n"
        weekly_matchup = self.league.weekly_matchup()
        for matchup in weekly_matchup.values():
            print_standing += (self.league.team_name_dict[matchup[0]] + " - " + str(matchup[1]) + "\n"
                               + self.league.team_name_dict[matchup[2]] + " - " + str(matchup[3]) + "\n\n")
        return print_standing

    def winners_bracket(self):
        return self.bracket(self.league.api.get_winners_bracket(), "Winners")

    def losers_bracket(self):
        return self.bracket(self.league.api.get_losers_bracket(), "Losers")

    def bracket(self, bracket, name):
        print_wbs = None
        if not self.league.is_season_complete():
            winner, loser = "winner", "loser"
            if name == "Losers": winner, loser = "loser", "winner"
            print_wbs = name + " Bracket \n\n"
            team1, team2 = "team1", "team2"
            for matchup in bracket:
                if matchup['w'] is None:
                    print_wbs += "Round " + str(matchup['r']) + " - Matchup " + str(matchup['m']) + "\n"
                    if matchup['t1'] is not None:
                        team1 = self.league.team_name_dict[matchup['t1']]
                    elif 't1_from' in matchup and matchup['t1_from'] is not None:
                        if 'w' in matchup['t1_from']:
                            team1 = winner + " of matchup " + str(matchup['t1_from']['w'])
                        elif 'l' in matchup['t1_from']:
                            team1 = loser + " of matchup " + str(matchup['t1_from']['l'])
                    if matchup['t2'] is not None:
                        team2 = self.league.team_name_dict[matchup['t2']]
                    elif 't2_from' in matchup and matchup['t2_from'] is not None:
                        if 'w' in matchup['t2_from']:
                            team2 = winner + " of matchup " + str(matchup['t2_from']['w'])
                        elif 'l' in matchup['t1_from']:
                            team2 = loser + " of matchup " + str(matchup['t2_from']['l'])
                print_wbs += team1 + " vs " + team2 + "\n\n"
        return print_wbs

    def winners_bracket_prediction(self):
        print_wbps = None
        if not self.league.is_season_complete():
            print_wbps = "Winners Bracket Champion Probability:\n\n"
            for team_id, playoff_pred in self.league.winners_bracket_prediction():
                print_wbps += self.league.team_name_dict[team_id] + " " + str((100 * playoff_pred).round(2)) + " %\n"
        return print_wbps

    def losers_bracket_prediction(self):
        print_wbps = None
        if not self.league.is_season_complete():
            print_wbps = "Losers Bracket Toilet Bowl Probability:\n\n"
            for team_id, playoff_pred in self.league.losers_bracket_prediction():
                print_wbps += self.league.team_name_dict[team_id] + " " + str((100 * playoff_pred).round(2)) + " %\n"
        return print_wbps

    def weekly_volatility(self):
        print_std = "Weekly Volatility:\n\n"
        team_stds = {}
        for team in self.league.team_name_dict:
            team_stds[team] = self.league.generate_predicted_points(team)
        for team_std in sorted(team_stds.items(), key=lambda x: x[1]):
            print_std += team_std[0] + " - " + str(team_std[1].round(2)) + "\n"
        return print_std

    def best_division(self):
        if self.league.has_divisions():
            print_div = self.league.get_division_1_name() + " vs " + self.league.get_division_2_name() + \
                        " (Week " + str(self.league.current_week - 1) + "):\n\n{}\n{} - {}\n{} - {}\n"
            div1, div2 = self.league.best_division()
            if div1 > div2:
                return print_div.format(self.league.get_division_1_name() + " win!!", self.league.get_division_1_name(),
                                        div1, self.league.get_division_2_name(), div2)
            elif div2 > div1:
                return print_div.format(self.league.get_division_2_name() + " win!!", self.league.get_division_2_name(),
                                        div2, self.league.get_division_1_name(), div1)
            else:
                return print_div.format("It's a tie!!", self.league.get_division_1_name(), div1,
                                        self.league.get_division_2_name(), div2)

