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

POSITIVE_REACTIONS = [
  "+1",
  "the_horns",
  "metal",
  "raised_hands",
  "ok",
  "ok_hand",
  "fire",
  "tada",
  "confetti_ball"
]

NEGATIVE_REACTIONS = ["-1", "middle_finger"]

PRIVILEGED_COMMANDS = ["undoteams", "generate", "autoupdate"]

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
