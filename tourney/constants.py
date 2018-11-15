import sys
from datetime import time, timedelta

# Will print all read events to stdout.
DEBUG = False

# In demo mode, no connection to slack is made. Everything is local.
DEMO = "--demo" in sys.argv

# A load test will stop the program right after initializing and before starting the REPL.
LOAD_TEST = "--load-test" in sys.argv

DATA_PATH = "~/.tourney"

CHANNEL_NAME = "foosball"
RTM_READ_DELAY = 0.5  # seconds
RECONNECT_DELAY = 5.0  # seconds

COMMAND_REGEX = "!(\\w+)\\s*(.*)"
REACTION_REGEX = ":(.+):"
SCORE_ARGS_REGEX = "(T\\d+)\\s+(\\d+)\\s+(T\\d+)\\s+(\\d+)"
WIN_ARGS_REGEX = "(\\d+)\\s+(\\d+)"

STATS_DAYS_BACK = 60
STATS_PLACEMENT_DELTA = 1

MORNING_ANNOUNCE = time(9)
MORNING_ANNOUNCE_DELTA = timedelta(hours=1)

REMINDER_ANNOUNCE = time(11)
REMINDER_ANNOUNCE_DELTA = timedelta(minutes=49)

MIDDAY_ANNOUNCE = time(11, 50)
MIDDAY_ANNOUNCE_DELTA = timedelta(minutes=10)

NIGHT_CLEARING = time(23)
NIGHT_CLEARING_DELTA = timedelta(minutes=59)

POSITIVE_REACTIONS = [
  "+1",
  "the_horns",
  "metal",
  "raised_hands",
  "ok",
  "ok_hand",
  "fire",
  "tada",
  "confetti_ball",
  "man-gesturing-ok",
  "woman-gesturing-ok"
]

NEGATIVE_REACTIONS = [
  "-1",
  "middle_finger",
  "man-gesturing-no",
  "woman-gesturing-no"
]

PRIVILEGED_COMMANDS = ["undoteams", "generate", "autoupdate", "speak"]

TEAM_NAMES = [
  "Air Farce",
  "Cereal Killers",
  "Dangerous Dynamos",
  "Designated Drinkers",
  "Fire Breaking Rubber Duckies",
  "Game of Throw-ins",
  "Injured Reserve",
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
  "Thunderpants",
]

TEAM_NAME_DECORATIONS = [
    lambda x: "{} of Doom".format(x),
    lambda x: "{} +1".format(x),
    lambda x: "{} (Handicapped)".format(x),
    lambda x: "{} in the Membrane".format(x),
    lambda x: "{} on the Rocks".format(x),
    lambda x: " {} et al.".format(x),
    lambda x: "{} With Bells On".format(x),
    lambda x: "{}, Cherry on Top".format(x),
    lambda x: "Not {}".format(x),
    lambda x: "{}²".format(x),
    lambda x: "Blessed {}".format(x),
    lambda x: "Cursed {}".format(x),
    lambda x: "Punished {}".format(x),
    lambda x: "Shin {}".format(x),
    lambda x: "{} 2: Son of {}".format(x, x),
    lambda x: "Bride of {}".format(x),
    lambda x: "\"{}\"".format(x),
    lambda x: x.upper(),
    lambda x: x[::2],
    lambda x: x[::-1].lower().title(),
]
