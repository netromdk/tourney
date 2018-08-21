from datetime import time

# Will print all read events to stdout.
DEBUG = False

DATA_PATH = "~/.tourney"

CHANNEL_NAME = "foosball"
RTM_READ_DELAY = 0.5 # seconds

COMMAND_REGEX = "!(\\w+)\\s*(.*)"
REACTION_REGEX = ":(.+):"
SCORE_ARGS_REGEX = "(T\\d+)\\s+(\\d+)\\s+(T\\d+)\\s+(\\d+)"

MORNING_ANNOUNCE = time(9)
REMINDER_ANNOUNCE = time(11)
MIDDAY_ANNOUNCE = time(11, 50)

POSITIVE_REACTIONS = ["+1", "the_horns", "metal", "raised_hands", "ok", "ok_hand", "fire"]
NEGATIVE_REACTIONS = ["-1", "middle_finger"]

PRIVILEGED_COMMANDS = ["undoteams"]
