import os
import re
import subprocess
from time import sleep
from datetime import datetime, date
from random import shuffle
from slackclient import SlackClient

from .command import Command
from .help_command import HelpCommand
from .list_command import ListCommand
from .join_command import JoinCommand
from .leave_command import LeaveCommand
from .score_command import ScoreCommand
from .win_command import WinCommand
from .lose_command import LoseCommand
from .stats_command import StatsCommand
from .mystats_command import MyStatsCommand
from .undoteams_command import UndoTeamsCommand
from .state import State
from .lookup import Lookup
from .constants import *
from .scores import Scores
from .config import Config
from .stats import Stats

client = SlackClient(os.environ.get("TOURNEY_BOT_TOKEN"))
lookup = Lookup(client)

def create_teams():
  """Create teams and random team names."""
  participants = State.get().participants()
  amount = len(participants)
  if amount < 4:
    return None, None
  lst = participants
  for i in range(3):
    shuffle(lst)
  teams = [lst[i:i+2] for i in range(0, amount, 2)]

  # Make last team of three persons if not even number.
  if amount % 2 != 0:
    teams[-2].append(teams[-1][0])
    del(teams[-1])

  names = TEAM_NAMES
  shuffle(names)
  return teams, names[0:len(teams)]

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
  state = State.get()
  response = "<!channel>\n"
  teams, names = create_teams()
  unrecorded_matches = []
  if teams is None:
    response += "No games possible! At least 4 players are required!"
  else:
    response += "{} teams: ".format(len(teams))
    for i in range(len(teams)):
      fmt = ", ".join([lookup.user_name_by_id(uid) for uid in teams[i]])
      name = names[i]
      response += "\n\t[T{}] *{}*: {}".format(i, name, fmt)
    sched = create_schedule(len(teams))
    response += "\n\nSchedule:"
    for match in sched:
      plural = "s" if match[2] > 1 else ""
      name_a = names[match[0]]
      name_b = names[match[1]]
      response += "\n\t[T{}] *{}* vs. [T{}] *{}* ({} round{})".\
        format(match[0], name_a, match[1], name_b, match[2], plural)
      key = [match[0], match[1]]
      key.sort()
      unrecorded_matches.append(key)

    # Remember teams and unrecorded matches but clear participants and morning announce.
    state.set_teams(teams)
    state.set_team_names(names)
    state.set_unrecorded_matches(unrecorded_matches)
    state.set_participants([])
    state.set_morning_announce(None)
    state.save()

  channel_id = state.channel_id()
  client.api_call("chat.postMessage", channel=channel_id, text=response)

def parse_command(event):
  msg = event["text"].strip()
  user_id = event["user"]
  channel = event["channel"]

  m = re.match(COMMAND_REGEX, msg)
  if not m:
    return None

  command = m.group(1).lower()
  args = m.group(2).strip()

  cmd = None
  if command == "help":
    cmd = HelpCommand()
  elif command == "list":
    cmd = ListCommand()
  elif command == "join":
    cmd = JoinCommand()
  elif command == "leave":
    cmd = LeaveCommand()
  elif command == "score":
    cmd = ScoreCommand()
  elif command == "win":
    cmd = WinCommand()
  elif command == "lose":
    cmd = LoseCommand()
  elif command == "stats":
    cmd = StatsCommand()
  elif command == "mystats":
    cmd = MyStatsCommand()
  elif command == "undoteams":
    cmd = UndoTeamsCommand()

  # Special command handling.
  elif command == "generate":
    create_matches()
  elif command == "autoupdate":
    subprocess.Popen(["/bin/sh", "autoupdate.sh"])
    exit(0)

  if cmd is None:
    return None

  cmd.set_user_id(user_id)
  cmd.set_args(args)
  cmd.set_channel(channel)
  return cmd

def parse_events(events):
  for event in events:
    event_type = event["type"]

    # Handle commands.
    if event_type == "message" and not "subtype" in event:
      msg = event["text"].strip()
      user_id = event["user"]

      # Parse command.
      cmd = parse_command(event)
      if cmd:
        handle_command(cmd)
        continue

      m = re.match(REACTION_REGEX, msg)
      if m:
        reaction = m.group(1)
        if reaction in POSITIVE_REACTIONS:
          handle_command(Command(user_id, "join"))
        elif reaction in NEGATIVE_REACTIONS:
          handle_command(Command(user_id, "leave"))

    # Adding a positive reaction to morning or reminder announce message will join game, negative
    # will leave game, and removing reaction will do the opposite action.
    elif event_type == "reaction_added" or event_type == "reaction_removed":
      added = (event_type == "reaction_added")
      pos = (event["reaction"] in POSITIVE_REACTIONS)
      neg = (event["reaction"] in NEGATIVE_REACTIONS)
      ts = event["item"]["ts"]
      state = State.get()
      if ts == state.morning_announce() or ts == state.reminder_announce():
        if (added and pos) or (not added and neg):
          handle_command(Command(event["user"], "join"))
        elif (added and neg) or (not added and pos):
          handle_command(Command(event["user"], "leave"))

def handle_command(cmd):
  user_id = cmd.user_id()
  user_name = lookup.user_name_by_id(user_id)
  command = cmd.name()
  ephemeral = cmd.ephemeral()
  state = State.get()
  channel_id = cmd.channel()
  if not channel_id:
    channel_id = state.channel_id()
  participants = state.participants()

  response = None
  if not cmd.allowed():
    response = "`!{}` is a privileged command and you're not allowed to use it!".format(command)
  else:
    response = cmd.execute(lookup)

  if response is None:
    response = "Unknown command! Try `!help` for supported commands."

  if ephemeral:
    client.api_call("chat.postEphemeral", channel=channel_id, text=response, user=user_id)
  else:
    client.api_call("chat.postMessage", channel=channel_id, text=response)

def scheduled_actions():
  """Execute actions at scheduled times."""

  # Ignore on saturdays and sundays.
  now = datetime.today()
  if now.weekday() >= 5:
    return

  state = State.get()
  channel_id = state.channel_id()

  # Morning announcement for participants to join game.
  start = datetime.combine(date.today(), MORNING_ANNOUNCE)
  end = start + MORNING_ANNOUNCE_DELTA
  if now >= start and now < end and not state.morning_announce():
    resp = client.api_call("chat.postMessage", channel=channel_id,
      text="<!channel> Remember to join today's game before 11:50 by using `!join` or :+1: "
           "reaction to this message!")
    state.set_morning_announce(resp["ts"])
    state.save()

  # Reminder announcement for remaining participants to join game.
  start = datetime.combine(date.today(), REMINDER_ANNOUNCE)
  end = start + REMINDER_ANNOUNCE_DELTA
  if now >= start and now < end and not state.reminder_announce():
    scores = Scores.get()
    remaining = scores.recent_users(7) - set(state.participants())
    if len(remaining) == 0:
      print("No one to remind!")
      # Something that won't match timestamp but still isn't None.
      state.set_reminder_announce(1)
    else:
      fmt = ", ".join(["<@{}>".format(uid) for uid in remaining])
      resp = client.api_call("chat.postMessage", channel=channel_id,
        text="{} Remember to join today's game before 11:50 by using `!join` or :+1: "
             "reaction to this message!".format(fmt))
      state.set_reminder_announce(resp["ts"])
    state.save()
  elif now > end and state.reminder_announce():
    print("Clearing reminder announce")
    state.set_reminder_announce(None)
    state.save()

  # Midday announcement of game.
  start = datetime.combine(date.today(), MIDDAY_ANNOUNCE)
  end = start + MIDDAY_ANNOUNCE_DELTA
  if now >= start and now < end and not state.midday_announce():
    state.set_midday_announce(True)
    state.save()
    create_matches()
  elif now > end and state.midday_announce():
    print("Clearing midday announce")
    state.set_midday_announce(False)
    state.save()

def connect():
  delay = RECONNECT_DELAY
  while True:
    try:
      # After successful connection, reconnect if connection drops.
      ret = client.rtm_connect(reconnect=True, auto_reconnect=True, with_team_state=False)
      if ret:
        print("Connected!")
        break
    except Exception as ex:
      print(ex)

    print("Could not connect, retrying in {} seconds..".format(delay))
    sleep(delay)

def init():
  config = Config.get()
  state = State.get()
  scores = Scores.get()
  stats = Stats.get()

  if len(config.privileged_users()) == 0:
    print("No privileged users defined in config!")

  if state.bot_id() is None:
    state.set_bot_id(client.api_call("auth.test")["user_id"])
  print("Tourney bot ID: {}".format(state.bot_id()))

  # Find the channel ID of designated channel name.
  if state.channel_id() is None:
    channel_id = lookup.channel_id_by_name(CHANNEL_NAME)
    if channel_id is None:
      print("Could not find ID for channel: {}".format(CHANNEL_NAME))
      exit(1)
    state.set_channel_id(channel_id)
  print("#{} channel ID: {}".format(CHANNEL_NAME, state.channel_id()))

  state.save()

def repl():
  print("Entering REPL..")
  while True:
    scheduled_actions()
    events = client.rtm_read()
    if DEBUG:
      print(events)
    parse_events(events)
    sleep(RTM_READ_DELAY)

def start_tourney():
  connect()
  init()
  repl()
