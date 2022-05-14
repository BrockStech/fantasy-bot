from src.message import GroupMe
from src.formatter import Formatter
from src.user_input_handler import group_me_bot_id, post_type
from src.sacko_bot import *
import datetime
import random

MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7)


class MessageScheduler:
    def __init__(self):
        self.week_day = datetime.datetime.today().weekday()
        self.formatter = Formatter()
        self.messages = []
        self.group_me_bot = None

    def post_messages(self):
        message_post_type = post_type()
        if message_post_type == "sacko":
            self.post_sacko_message()
        elif self.is_season_in_progress():
            if message_post_type == "schedule":
                self.post_by_schedule()
            elif message_post_type == "test":
                self.post_test()
            else:
                self.post_all()
        else:
            print("Season has completed. See you again next year!!\n")
            
    def post_by_schedule(self):
        if self.week_day == TUESDAY:
            if self.formatter.league.current_week > 1:
                self.messages.append(self.formatter.standings())
                self.messages.append(self.formatter.best_division())
            if self.formatter.league.current_week > 2:
                self.messages.append(self.formatter.weekly_volatility())
            if self.is_season_past_midpoint():
                self.messages.append(self.formatter.winners_bracket())
                self.messages.append(self.formatter.losers_bracket())
        elif self.week_day == WEDNESDAY:
            self.messages.append(self.formatter.faab())
            if self.formatter.league.current_week > 1:
                self.messages.append(self.formatter.predicted_playoff_standings())
        elif self.week_day == THURSDAY:
            self.messages.append(self.formatter.matchup())
            if self.is_season_past_midpoint():
                self.messages.append(self.formatter.winners_bracket_prediction())
                self.messages.append(self.formatter.losers_bracket_prediction())
        self.process_messages(self.messages)

    def post_nba(self):
        if self.week_day == MONDAY:
            self.messages.append(self.formatter.standings())
            self.messages.append(self.formatter.faab())
            self.messages.append(self.formatter.matchup())
            self.messages.append(self.formatter.predicted_playoff_standings())
        if self.week_day == TUESDAY:
            if self.is_season_past_midpoint():
                self.messages.append(self.formatter.winners_bracket())
                self.messages.append(self.formatter.losers_bracket())
                self.messages.append(self.formatter.winners_bracket_prediction())
                self.messages.append(self.formatter.losers_bracket_prediction())
        self.messages.append(self.formatter.scoreboard())
        self.process_messages(self.messages)

    def post_all(self):
        self.messages.append(self.formatter.standings())
        self.messages.append(self.formatter.faab())
        self.messages.append(self.formatter.matchup())
        self.messages.append(self.formatter.scoreboard())
        self.messages.append(self.formatter.predicted_playoff_standings())
        if self.is_season_past_midpoint():
            self.messages.append(self.formatter.winners_bracket())
            self.messages.append(self.formatter.losers_bracket())
            self.messages.append(self.formatter.winners_bracket_prediction())
            self.messages.append(self.formatter.losers_bracket_prediction())
        self.process_messages(self.messages)

    # TODO
    def post_test(self):
        self.messages.append(self.formatter.winners_bracket_prediction())
        self.messages.append(self.formatter.losers_bracket_prediction())
        self.process_messages(self.messages)

    def post_sacko_message(self):
        selection = random.choice([1, 2])
        if selection == 1:
            self.messages.append(post_sacko_message())
        elif selection == 2:
            self.messages.append(post_sacko_jama())
        self.process_messages(self.messages)

    def is_season_in_progress(self):
        return self.formatter.league.season_in_progress() and self.formatter.league.current_week > 2 and not self.formatter.league.is_season_complete()

    def is_season_past_midpoint(self):
        return self.formatter.league.current_week > self.formatter.league.get_playoff_week_start() / 2

    def process_messages(self, messages):
        post_message = self.is_group_me_post()
        for message in messages:
            if message is not None:
                if post_message:
                    if isinstance(message, str):
                        response = self.group_me_bot.post_message(message)
                    else:
                        response = self.group_me_bot.post_image(message[0], message[1])
                    if 404 == response.status_code:
                        post_message = False
                        print("Error: Invalid GroupMe bot ID -- Printing results in terminal\n\n" + message)
                else:
                    print(message)

    def is_group_me_post(self):
        bot_id = group_me_bot_id()
        if bot_id is not None:
            self.group_me_bot = GroupMe(bot_id)
            return True
        return False


