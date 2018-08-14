import os
import time
import re
from datetime import datetime
from random import shuffle
from slackclient import SlackClient

from .command import Command

client = SlackClient(os.environ.get("TOURNEY_BOT_TOKEN"))
bot_id = None
channel_id = None
all_channels = None
all_users = {}
participants = []
morning_announce = None # Will contain ts of announcement message.
midday_announce = False

DEBUG = False
CHANNEL_NAME = "foosball"
RTM_READ_DELAY = 0.5 # seconds
COMMAND_REGEX = "!(\\w+)\\s*(.*)"
MORNING_ANNOUNCE_HOUR = 9
MIDDAY_ANNOUNCE_HOUR = 11
MIDDAY_ANNOUNCE_MINUTE = 50
POSITIVE_REACTIONS = ["+1", "the_horns", "metal", "raised_hands", "ok", "ok_hand"]
NEGATIVE_REACTIONS = ["-1", "middle_finger"]

def get_channels():
  return client.api_call("channels.list", exclude_archived=1, exclude_members=1)["channels"]

def lookup_channel_name(name):
  for channel in all_channels:
    if channel["name"] == name:
      return channel["id"]
  return None

def get_users():
  return client.api_call("users.list")["members"]

def lookup_user_name(user_id):
  if not user_id in all_users:
    return user_id
  return all_users[user_id]["name"]

def create_teams():
  amount = len(participants)
  if amount < 4:
    return None
  lst = participants
  for i in range(3):
    shuffle(lst)
  teams = [lst[i:i+2] for i in range(0, amount, 2)]
  # Make last team of three persons if not even number.
  if amount % 2 != 0:
    teams[-2].append(teams[-1][0])
    del(teams[-1])
  return teams

def pick_pairs(amount):
  """Picks non-overlapping team pairs of 2 rounds."""
  return [(i,i+1,2) for i in range(0, amount, 2)]

def create_schedule(amount):
  """Takes amount of teams to schedule for."""
  matches = []
  if amount % 2 == 0:
    matches = pick_pairs(amount)
  else:
    twoRoundMathces = amount - 3
    if twoRoundMathces > 0:
      matches = pick_pairs(twoRoundMathces)
    # Add last 3 matches of 1 round each.
    i = twoRoundMathces
    matches += [(i,i+1,1), (i,i+2,1), (i+1,i+2,1)]
  return matches

def create_matches():
  response = "<!channel>\n"
  teams = create_teams()
  if teams is None:
    response += "Could not create teams! There must be at least 4 participants!"
  else:
    response += "{} teams: ".format(len(teams))
    for i in range(len(teams)):
      fmt = ", ".join([lookup_user_name(uid) for uid in teams[i]])
      response += "\n\t*T{}*: {}".format(i, fmt)
    sched = create_schedule(len(teams))
    response += "\n\nSchedule:"
    for match in sched:
      plural = "s" if match[2] > 1 else ""
      response += "\n\t*T{}* vs. *T{}* ({} round{})".format(match[0], match[1], match[2], plural)
    participants.clear()
  client.api_call("chat.postMessage", channel=channel_id, text=response)

def parse_events(events):
  for event in events:
    event_type = event["type"]

    # Handle commands.
    if event_type == "message" and not "subtype" in event:
      msg = event["text"].strip()
      m = re.match(COMMAND_REGEX, msg)
      if m:
        handle_command(Command(event["user"], m.group(1), m.group(2).strip()))

    # Adding a positive reaction to morning announce message will join game, negative will leave
    # game, and removing reaction will do the opposite action.
    elif event_type == "reaction_added" or event_type == "reaction_removed":
      added = (event_type == "reaction_added")
      pos = (event["reaction"] in POSITIVE_REACTIONS)
      neg = (event["reaction"] in NEGATIVE_REACTIONS)
      if event["item"]["ts"] == morning_announce:
        if (added and pos) or (not added and neg):
          handle_command(Command(event["user"], "join"))
        elif (added and neg) or (not added and pos):
          handle_command(Command(event["user"], "leave"))

def handle_command(cmd):
  response = None
  user_id = cmd.user_id
  user_name = lookup_user_name(user_id)
  command = cmd.command
  ephemeral = True

  if command.startswith("help"):
    response = """
As the foosball bot, I accept the following commands:
  `!help` - Shows this text.
  `!list` - List users that joined game of the day.
  `!join` - Join game of the day.
  `!leave` - Leave game of the day.
"""
  elif command.startswith("list"):
    ephemeral = False
    amount = len(participants)
    if amount == 0:
      response = "No participants have joined yet!"
    else:
      response = "List of {} participants for game of the day:".format(amount)
      for uid in participants:
        name = lookup_user_name(uid)
        response += "\n{}".format(name)
  elif command.startswith("join"):
    if user_id not in participants:
      participants.append(user_id)
      response = "{}, you've joined today's game!".format(user_name)
    else:
      response = "{}, you've _already_ joined today's game!".format(user_name)
  elif command.startswith("leave"):
    if user_id not in participants:
      response = "{}, you've _not_ joined today's game!".format(user_name)
    else:
      participants.remove(user_id)
      response = "{}, you've left today's game!".format(user_name)

  if response is None:
    response = "Unknown command! Try `!help` for supported commands."

  if ephemeral:
    client.api_call("chat.postEphemeral", channel=channel_id, text=response, user=user_id)
  else:
    client.api_call("chat.postMessage", channel=channel_id, text=response)

def scheduled_actions():
  """Execute actions at scheduled times."""
  global morning_announce, midday_announce
  now = datetime.today()

  # Ignore on saturdays and sundays.
  if now.weekday() >= 5:
    return

  h = now.hour
  m = now.minute
  if h >= MORNING_ANNOUNCE_HOUR and h < MORNING_ANNOUNCE_HOUR+1 and morning_announce is None:
    resp = client.api_call("chat.postMessage", channel=channel_id,
      text="<!channel> Remember to join today's game before 11:50 by using `!join` or :+1: "
           "reaction to this message!")
    morning_announce = resp["ts"]
  if h >= MIDDAY_ANNOUNCE_HOUR and h < MIDDAY_ANNOUNCE_HOUR+1 and m >= MIDDAY_ANNOUNCE_MINUTE and \
     not midday_announce:
    midday_announce = True
    create_matches()

def connect():
  if not client.rtm_connect(with_team_state=False):
    print("Could not connect to Slack!")
    exit(1)

  print("Connected!")

def init():
  bot_id = client.api_call("auth.test")["user_id"]
  print("Tourney bot ID: {}".format(bot_id))

  # Find the channel ID of designated channel name.
  global all_channels
  all_channels = get_channels()
  global channel_id
  channel_id = lookup_channel_name(CHANNEL_NAME)
  if channel_id is None:
    print("Could not find ID for channel: {}".format(CHANNEL_NAME))
    exit(1)
  print("#{} channel ID: {}".format(CHANNEL_NAME, channel_id))

  # Map user IDs to their info.
  for user in get_users():
    all_users[user["id"]] = user
  print("Detected {} users..".format(len(all_users)))

def repl():
  print("Entering REPL..")
  while True:
    scheduled_actions()
    events = client.rtm_read()
    if DEBUG:
      print(events)
    parse_events(events)
    time.sleep(RTM_READ_DELAY)

def start_tourney():
  connect()
  init()
  repl()
