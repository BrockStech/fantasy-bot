import unittest
from src.message import GroupMe

fake_bot_id = "5555a1a2bd6aa0881a7fee3c2f"


class TestGroupMe(unittest.TestCase):
    def test_false_group_me_bot(self):
        group_me_bot = GroupMe(fake_bot_id)
        response = group_me_bot.post_message("TEST MESSAGE")
        self.assertEqual(response.status_code, 404)
