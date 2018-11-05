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
