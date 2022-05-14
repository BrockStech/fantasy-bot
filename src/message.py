import requests


class GroupMe:
    def __init__(self, bot_id):
        self.bot_id = bot_id

    def post_message(self, message):
        return requests.post("https://api.groupme.com/v3/bots/post",
                             json={"text": message, "bot_id": self.bot_id})

    def post_image(self, message, image_url):
        return requests.post("https://api.groupme.com/v3/bots/post",
                             json={"text": message, "bot_id": self.bot_id,
                                   "picture_url": image_url})
