import sys
from datetime import time, timedelta

# Special seasons, with off-season mixin chance
SEASONS = {"easter": 0.01, "halloween": 0.1, "xmas": 0.05}
SEASON = None

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

# Preferred number of rounds in cases where one or two could be played
PREFERRED_ROUNDS = 1

POSITIVE_REACTIONS = [
  "+1",
  "accept",
  "arrow_forward",
  "ballot_box_with_check",
  "boom",
  "chaos",
  "confetti_ball",
  "dance",
  "dizzy",
  "fire",
  "flag-dk",
  "heavy_check_mark",
  "heavy_plus_sign",
  "here",
  "keyvr",
  "ks",
  "man-gesturing-ok",
  "man-raising-hand",
  "metal",
  "ok",
  "ok_hand",
  "party_parrot",
  "pirate_flag",
  "raised_hands",
  "raising_hand",
  "soccer",
  "tada",
  "the_horns",
  "thumbsup",
  "thumbsup_all",
  "white_check_mark",
  "woman-gesturing-ok",
  "woman-raising-hand",
]

NEGATIVE_REACTIONS = [
  "-1",
  "away",
  "black_square_for_stop",
  "heavy_minus_sign",
  "man-gesturing-no",
  "negative_squared_cross_mark",
  "no_bell",
  "no_entry",
  "no_entry_sign",
  "see_no_evil",
  "stahp",
  "thumbsdown",
  "woman-gesturing-no",
  "x",
]

DEFENSE_EMOTE = 'shield'
OFFENSE_EMOTE = 'crossed_swords'
ROTATE_EMOTE = 'repeat'
SOLO_EMOTES = [
  'unicorn_face',
  'muscle',
  'godmode',
  'weight_lifter',
  'sweat_drops']

PRIVILEGED_COMMANDS = [
  "autoupdate",
  "generate",
  "speak",
  "startseason",
  "undoteams",
]
