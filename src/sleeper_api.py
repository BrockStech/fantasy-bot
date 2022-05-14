import requests
import requests_cache

requests_cache.install_cache(cache_name='sleeper_cache', backend='sqlite', expire_after=3600)


class SleeperApi:
    def __init__(self, league_id):
        self._base_url = "https://api.sleeper.app/v1/league/{}".format(league_id)

    def get_status(self):
        return self.request_url(self._base_url).raise_for_status()

    def get_league(self):
        return self.call(self._base_url)

    def get_users(self):
        return self.call("{}/{}".format(self._base_url, "users"))

    def get_rosters(self):
        return self.call("{}/{}".format(self._base_url, "rosters"))

    def get_matchups(self, week):
        return self.call("{}/{}/{}".format(self._base_url, "matchups", week))

    def get_winners_bracket(self):
        return self.call("{}/{}".format(self._base_url, "winners_bracket"))

    def get_state(self):
        return self.call("{}/{}".format("https://api.sleeper.app/v1/", "state/nfl"))

    def get_losers_bracket(self):
        return self.call("{}/{}".format(self._base_url, "losers_bracket"))

    def call(self, url):
        result_json = self.request_json(url)
        max_retry = 10
        while result_json is None:
            result_json = self.request_json(url)
            if max_retry <= 0: return
            max_retry -= 1
        return result_json

    def request_json(self, url):
        result_json_string = self.request_url(url)
        try:
            result_json_string.raise_for_status()
        except requests.exceptions.HTTPError:
            return None
        return result_json_string.json()

    @staticmethod
    def request_url(url):
        return requests.get(url)

