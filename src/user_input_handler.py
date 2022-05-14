from .sleeper_api import SleeperApi
from requests.exceptions import HTTPError
import sys

default_sleeper_league = 289646328504385536


def sleeper_league_id():
    usage()
    try:
        if sys.argv[1] is None:
            league_id = int(input("Enter your Sleeper league ID (press enter for default): "))
        else:
            league_id = int(sys.argv[1])
        validate(league_id)
    except (ValueError, IndexError, HTTPError):
        print("Using default Sleeper league ID - See usage for more information\n")
        league_id = default_sleeper_league
    return league_id


def validate(league_id):
    api = SleeperApi(league_id)
    api.get_status()
    print("Sleeper league " + api.get_league()["name"] + " found!\n")


def group_me_bot_id():
    try:
        if sys.argv[2] is None:
            bot_id = str(input("Enter your GroupMe bot ID (press enter for default): "))
        else:
            bot_id = str(sys.argv[2])
    except (ValueError, IndexError, HTTPError):
        print("Using default - See usage for more information\n")
        bot_id = None
    return bot_id


def post_type():
    try:
        message_post_type = str(sys.argv[3]).lower()
    except (ValueError, IndexError):
        message_post_type = "all"
    return message_post_type


def usage():
    if len(sys.argv) <= 1:
        print("----- Usage -----\nParameters:\n1. Sleeper league ID (Default - Sleeper's sample league)\n    "
              "- Can be found in the URL of your sleeper home page\n"
              "2. GroupMe bot ID (Default - Prints results to terminal)\n    "
              "- Bots can be created here -> https://dev.groupme.com/bots/new\n"
              "3. Determine which league statistics you want to post/view (Default - post all statistics)\n"
              "    - \"schedule\" statistics are posted based on the day of the week\n        "
              "-- Ex: Standings are posted on Tuesday. Remaining FAAB is posted on Wednesday\n"
              "    - \"all\" posts all available statistics\n"
              "Usage: python main.py <League ID> <GroupMe Bot ID> <Post Type>\n")
