import random

sacko_message = ["Analytics don't win fantasy leagues!",
                 "Still think fantasy football is all skill?",
                 "Hopefully Luke is better at driving than fantasy football",
                 "Fun fact: Luke has been sacko 25% of the time"]

sacko_gif = {
    "gig": "https://i.groupme.com/360x480.jpeg.3e3027e139714277956fa3486781cc74",
    "lake": "https://i.groupme.com/282x500.gif.fc4dcc06bed649d3b4d70506541f08c6",
    "pancaked": "https://i.groupme.com/750x1334.jpeg.fbf6b4c990794ceca3b576c1631254a5",
    "grills": "https://i.groupme.com/768x1024.jpeg.9ace3adb1ee34c66aa89ecb495bb3519"
}

division = {
    "tacos": ["Mancz", "Brock", "Luke", "Gavin", "Shawn", "Bingo"],
    "nachos": ["Shatz", "Divey", "Jama", "Zach", "Krep", "Shmoop"]
}

sacko = {
    "previous": "Mancz",
    "current": "Luke"
}


# The League (Dayton)
def post_sacko_message():
    return random.choice(sacko_message)


def post_sacko_gif_golf():
    return "8:00 AM Sacko Bot messages hitting Luke like", sacko_gif["golf_cart"]


def post_sacko_gif_dab():
    return "That Friday feeling", sacko_gif["dab"]


def post_sacko_gif_gig():
    return "The face you make when you realize you're the sacko", sacko_gif["gig"]


def post_sacko_gif_lake():
    return "TFW you lose to Shmoop's algorithm", sacko_gif["lake"]


def post_sacko_gif_pancaked():
    return "Two Sackos!", sacko_gif["pancaked"]


def post_sacko_gif_grills():
    return "Fantasy Tramp", sacko_gif["grills"]


def post_sacko_gif_turnt_up(result):
    if result > 0: return "Jama getting turnt up after a Luke " + str(result) + " point L", sacko_gif["turnt_up"]
