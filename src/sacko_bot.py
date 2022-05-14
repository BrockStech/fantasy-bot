import random

sacko_message = ["Go Blue!",
                 "Fun fact: Jama has been sacko 33% of the time"]

sacko_gif = {
    "jama": "https://i.groupme.com/531x960.jpeg.45548b95139245a0991a3ea97480937a"
}

division = {
    "tacos": ["Mancz", "Brock", "Luke", "Gavin", "Shawn", "Bingo"],
    "nachos": ["Shatz", "Divey", "Jama", "Zach", "Krep", "Shmoop"]
}

sacko = {
    "previous": "Luke",
    "current": "Jama"
}


# The League (Dayton)
def post_sacko_message():
    return random.choice(sacko_message)


# Mancz
def post_sacko_gif_golf():
    return "8:00 AM Sacko Bot messages hitting Mancz like", sacko_gif["golf_cart"]
# "golf_cart": "https://i.groupme.com/218x384.gif.3a772845b4664158b95b44b02d8b1e84"
# "turnt_up": "https://i.groupme.com/311x510.gif.6fc9805b0182404da93d801ef1c6bfc7"


# Luke
def post_sacko_gif_dab():
    return "That Friday feeling", sacko_gif["dab"]
# "gig": "https://i.groupme.com/360x480.jpeg.3e3027e139714277956fa3486781cc74",
# "lake": "https://i.groupme.com/282x500.gif.fc4dcc06bed649d3b4d70506541f08c6",
# "pancaked": "https://i.groupme.com/750x1334.jpeg.fbf6b4c990794ceca3b576c1631254a5",
# "grills": "https://i.groupme.com/768x1024.jpeg.9ace3adb1ee34c66aa89ecb495bb3519"


def post_sacko_gif_gig():
    return "The face you make when you realize you're the sacko", sacko_gif["gig"]


def post_sacko_gif_lake():
    return "TFW you lose to Shmoop's algorithm", sacko_gif["lake"]


def post_sacko_gif_pancaked():
    return "Two Sackos!", sacko_gif["pancaked"]


def post_sacko_gif_grills():
    return "Fantasy Tramp", sacko_gif["grills"]


# Jama
def post_sacko_jama():
    return "Three Sackos!", sacko_gif["jama"]


def post_sacko_gif_turnt_up(result):
    if result > 0: return "Jama getting turnt up after a Luke " + str(result) + " point L", sacko_gif["turnt_up"]
