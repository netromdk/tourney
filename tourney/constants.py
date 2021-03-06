import sys
from datetime import time, timedelta

# Will print all read events to stdout.
DEBUG = False

# In demo mode, no connection to slack is made. Everything is local.
DEMO = "--demo" in sys.argv

# Use trueskill to create schedule
MATCHMAKING = True

# A load test will stop the program right after initializing and before starting the REPL.
LOAD_TEST = "--load-test" in sys.argv

DATA_PATH = "~/.tourney"

CHANNEL_NAME = "foosball"
RTM_READ_DELAY = 0.5  # seconds
RECONNECT_DELAY = 5.0  # seconds

COMMAND_REGEX = "!(\\w+)\\s*(.*)"
REACTION_REGEX = ":(.+?):"  # non-greedy
SCORE_ARGS_REGEX = "(T\\d+)\\s+(\\d+)\\s+(T\\d+)\\s+(\\d+)"
WIN_ARGS_REGEX = "(\\d+)\\s+(\\d+)"

STATS_DAYS_BACK = 60
STATS_PLACEMENT_DELTA = 1
MEDAL_LIST = ["first_place_medal", "second_place_medal", "third_place_medal"]

MORNING_ANNOUNCE = time(9)
MORNING_ANNOUNCE_DELTA = timedelta(hours=1)

REMINDER_ANNOUNCE = time(11)
REMINDER_ANNOUNCE_DELTA = timedelta(minutes=30)

MIDDAY_ANNOUNCE = time(11, 55)
MIDDAY_ANNOUNCE_DELTA = timedelta(minutes=10)

NIGHT_CLEARING = time(23)
NIGHT_CLEARING_DELTA = timedelta(minutes=59)

POSITIVE_REACTIONS = [
  "+1",
  "arrow_forward",
  "ballot_box_with_check",
  "confetti_ball",
  "dance",
  "fire",
  "heavy_check_mark",
  "heavy_plus_sign",
  "ks",
  "man-gesturing-ok",
  "man-raising-hand",
  "metal",
  "ok",
  "ok_hand",
  "party_parrot",
  "raised_hands",
  "raising_hand",
  "soccer",
  "tada",
  "the_horns",
  "thumbsup_all",
  "white_check_mark",
  "woman-gesturing-ok",
  "woman-raising-hand",
]

NEGATIVE_REACTIONS = [
  "-1",
  "black_square_for_stop",
  "heavy_minus_sign",
  "man-gesturing-no",
  "middle_finger",
  "negative_squared_cross_mark",
  "no_entry",
  "no_entry_sign",
  "see_no_evil",
  "stahp",
  "woman-gesturing-no",
  "x",
]

PRIVILEGED_COMMANDS = [
  "autoupdate",
  "generate",
  "speak",
  "startseason",
  "undoteams",
]

TEAM_NAMES = [
  "Air Farce",
  "Cereal Killers",
  "Dangerous Dynamos",
  "Designated Drinkers",
  "Fantastic Four",
  "Fire Breaking Rubber Duckies",
  "Game of Throw-ins",
  "Glorious Bastards",
  "Injured Reserve",
  "Monkey Python",
  "One Hit Wonders",
  "Our Uniforms Match",
  "Pique Blinders",
  "Pistons from the Past",
  "Purple Cobras",
  "Rabid Squirrels",
  "Raging Nightmare",
  "Recipe for Disaster",
  "Shockwave",
  "Smarty Pints",
  "Straight off the Couch",
  "Tenacious Turtles",
  "The Abusement Park",
  "The Flaming Flamingos",
  "The League of Ordinary Gentlemen",
  "The Meme Team",
  "The Mullet Mafia",
  "Thunderpants"
]

TEAM_NAME_DECORATIONS = [
    lambda x: "{} of Doom".format(x),
    lambda x: "{} +1".format(x),
    lambda x: "{} (Handicapped)".format(x),
    lambda x: "{} in the Membrane".format(x),
    lambda x: "{} on the Rocks".format(x),
    lambda x: "{} et al.".format(x),
    lambda x: "{} With Bells On".format(x),
    lambda x: "{}, Cherry on Top".format(x),
    lambda x: "Not {}".format(x),
    lambda x: "{}²".format(x),
    lambda x: "Blessed {}".format(x),
    lambda x: "Cursed {}".format(x),
    lambda x: "Punished {}".format(x),
    lambda x: "Shin {}".format(x),
    lambda x: "{} Stranding".format(x),
    lambda x: "{} 2: Son of {}".format(x, x),
    lambda x: "Bride of {}".format(x),
    lambda x: "\"{}\"".format(x),
    lambda x: x.upper(),
    lambda x: x[::2],
    lambda x: x[::-1].lower().title(),
    lambda x: "I Can't Believe It's Not {}".format(x),
    lambda x: "".join([c if c.lower() not in "aeiouyæøå" else 'o' for c in x]),
]
