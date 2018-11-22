import os
import re
import subprocess  # nosec
from time import sleep
from datetime import datetime, date
from random import shuffle
from slackclient import SlackClient
import calendar

from .commands import HelpCommand, ListCommand, JoinCommand, LeaveCommand, ScoreCommand, \
  WinLoseCommand, StatsCommand, MyStatsCommand, UndoTeamsCommand, AchievementsCommand, \
  ResultsCommand, TeamsCommand, ScheduleCommand, AllStatsCommand
from .state import State
from .lookup import Lookup
from .constants import DEMO, TEAM_NAMES, COMMAND_REGEX, REACTION_REGEX, POSITIVE_REACTIONS, \
  NEGATIVE_REACTIONS, MORNING_ANNOUNCE, MORNING_ANNOUNCE_DELTA, REMINDER_ANNOUNCE, \
  REMINDER_ANNOUNCE_DELTA, MIDDAY_ANNOUNCE, MIDDAY_ANNOUNCE_DELTA, RECONNECT_DELAY, CHANNEL_NAME, \
  DEBUG, RTM_READ_DELAY, LOAD_TEST, NIGHT_CLEARING, NIGHT_CLEARING_DELTA
from .scores import Scores
from .config import Config
from .stats import Stats
from .util import command_allowed, unescape_text
from .achievements import Achievements, InvokeBehavior, LeaveChannelBehavior, SeasonStartBehavior

bot_token = os.environ.get("TOURNEY_BOT_TOKEN")
client = SlackClient(bot_token)
lookup = Lookup(client)

# Change functionality in demo mode so that invoking API calls just prints to stdout, and reading
# events blocks and asks on stdin.
if DEMO:
  def wrap_api_call(method, timeout=None, **kwargs):
    print("{} {}".format(method, unescape_text(str(kwargs))))
    return {}
  client.api_call = wrap_api_call

  def wrap_rtm_read():
    try:
      text = input("> ")  # nosec
    except KeyboardInterrupt:
      exit(0)
    except EOFError:
      exit(0)
    event = {
      "type": "message",
      "text": text,
      "user": "TESTUSER",
      "channel": "#DEMOCHANNEL"
    }
    return [event]
  client.rtm_read = wrap_rtm_read

def create_teams():
  """Create teams and random team names."""
  participants = State.get().participants()
  amount = len(participants)
  if amount < 4:
    return None, None
  lst = participants
  for i in range(3):
    shuffle(lst)
  teams = [lst[i:i + 2] for i in range(0, amount, 2)]

  # Make last team of three persons if not even number.
  if amount % 2 != 0:
    teams[-2].append(teams[-1][0])
    del(teams[-1])

  names = TEAM_NAMES
  shuffle(names)
  return teams, names[0:len(teams)]

def pick_pairs(amount):
  """Picks non-overlapping team pairs of 2 rounds."""
  return [(i, i + 1, 2) for i in range(0, amount, 2)]

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
    matches += [(i, i + 1, 1), (i, i + 2, 1), (i + 1, i + 2, 1)]
  return matches

def create_matches():
  state = State.get()
  response = "<!channel>\n"
  teams, names = create_teams()
  if teams is None:
    response += "No games possible! At least 4 players are required!"
  else:
    response += "{} teams: ".format(len(teams))
    for i in range(len(teams)):
      fmt = ", ".join([lookup.user_name_by_id(uid) for uid in teams[i]])
      name = names[i]
      response += "\n\t[T{}] *{}*: {}".format(i, name, fmt)

    sched = create_schedule(len(teams))
    unrecorded_matches = []

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

    # Remember teams and unrecorded matches but clear participants, morning announce, and users that
    # didn't want today's reminder.
    state.set_schedule(sched)
    state.set_teams(teams)
    state.set_team_names(names)
    state.set_unrecorded_matches(unrecorded_matches)
    state.set_participants([])
    state.set_morning_announce(None)
    state.set_dont_remind_users([])
    state.save()

  channel_id = state.channel_id()
  client.api_call("chat.postMessage", channel=channel_id, text=response)

# If not running as a service then execute "autoupdate.sh" that will git pull and run tourney.py
# again. Otherwise, it will run "update.sh" that will git pull only. In both cases this process will
# exit with code 0. Note that when running as a service it is extected that the service will respawn
# the process when it is terminated!
def autoupdate():
  client.api_call("chat.postMessage", channel=State.get().channel_id(),
                  text="Going offline to auto-update and restart..")
  cwd = os.getcwd()
  script = "autoupdate.sh"
  if Config.get().running_as_service():
    script = "update.sh"
  subprocess.run(["/bin/sh", script], cwd=cwd)  # nosec
  exit(0)

def parse_command(event):
  msg = event["text"].strip()
  user_id = event["user"]
  channel = event["channel"]
  achievements = Achievements.get()

  m = re.match(COMMAND_REGEX, msg)
  if not m:
    return None

  command = m.group(1).lower()
  args = m.group(2).strip()
  state = State.get()
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
    channel = state.channel_id()  # Always write response in main channel.
  elif command == "win" or command == "lose":
    cmd = WinLoseCommand(command)
    channel = state.channel_id()
  elif command == "stats":
    cmd = StatsCommand()
  elif command == "allstats":
    cmd = AllStatsCommand()
  elif command == "mystats":
    cmd = MyStatsCommand()
  elif command == "undoteams":
    cmd = UndoTeamsCommand()
    channel = state.channel_id()
  elif command == "achievements":
    cmd = AchievementsCommand()
  elif command == "acheivements":
    achievements.interact(InvokeBehavior(user_id, command))
  elif command == "results":
    cmd = ResultsCommand()
    channel = state.channel_id()
  elif command == "teams":
    cmd = TeamsCommand()
    channel = state.channel_id()
  elif command == "schedule":
    cmd = ScheduleCommand()
    channel = state.channel_id()

  # Special command handling.
  if command_allowed(command, user_id):
    if command == "generate":
      create_matches()
    elif command == "autoupdate":
      autoupdate()
    elif command == "speak" and len(args) > 0:
      client.api_call("chat.postMessage", channel=state.channel_id(), text=args)

  # Only send ephemeral message if command hasn't been parsed into a command instance because
  # `handle_command()` will do it otherwise.
  elif cmd is None:
    response = "`!{}` is a privileged command and you're not allowed to use it!".format(command)
    client.api_call("chat.postEphemeral", channel=channel, text=response, user=user_id)

  if cmd is None:
    return None

  cmd.set_user_id(user_id)
  cmd.set_args(args)
  cmd.set_channel(channel)
  return cmd

def parse_events(events):
  state = State.get()
  created_teams = len(state.teams()) > 0

  for event in events:
    event_type = event["type"]

    # Handle commands.
    if event_type == "message" and "subtype" not in event:
      msg = event["text"].strip()
      user_id = event["user"]
      channel_id = event["channel"]

      # Parse command.
      cmd = parse_command(event)
      if cmd:
        handle_command(cmd)
        continue

      # Join/leave game via reaction if not already started.
      m = re.match(REACTION_REGEX, msg)
      if m and not created_teams:
        reaction = m.group(1)
        if reaction in POSITIVE_REACTIONS:
          handle_command_direct("!join", user_id, channel_id)
        elif reaction in NEGATIVE_REACTIONS:
          handle_command_direct("!leave", user_id, channel_id)

    # Handle leaving channel.
    if event_type == "member_left_channel":
      user_id = event["user"]
      Achievements.get().interact(LeaveChannelBehavior(user_id))

    # Adding a positive reaction to morning or reminder announce message will join game, negative
    # will leave game, and removing reaction will do the opposite action. But only if game is not
    # already started.
    elif (event_type == "reaction_added" or event_type == "reaction_removed") \
         and not created_teams:
      added = (event_type == "reaction_added")
      pos = (event["reaction"] in POSITIVE_REACTIONS)
      neg = (event["reaction"] in NEGATIVE_REACTIONS)
      ts = event["item"]["ts"]
      channel = event["item"]["channel"]
      if ts == state.morning_announce() or ts == state.reminder_announce():
        if (added and pos) or (not added and neg):
          handle_command_direct("!join", event["user"], channel)
        elif (added and neg) or (not added and pos):
          handle_command_direct("!leave", event["user"], channel)

def handle_command_direct(cmd, user_id, channel_id=None):
  """Handle command in short hand style."""
  event = {}
  event["text"] = cmd
  event["user"] = user_id
  event["channel"] = State.get().channel_id()
  if channel_id is not None:
    event["channel"] = channel_id
  cmd = parse_command(event)
  if cmd:
    handle_command(cmd)

def handle_command(cmd):
  user_id = cmd.user_id()
  command = cmd.name()
  ephemeral = cmd.ephemeral()
  state = State.get()
  channel_id = cmd.channel()
  if not channel_id:
    channel_id = state.channel_id()
  achievements = Achievements.get()

  response = None
  if not cmd.allowed():
    response = "`!{}` is a privileged command and you're not allowed to use it!".format(command)
  else:
    response = cmd.execute(lookup)

    # Check if the response was deemed necessary to be made public, only for this execution.
    if cmd.public():
      print("Overriding response to be public")
      ephemeral = False
      channel_id = state.channel_id()

    # TODO: Should it only accept behavior if command executed without errors?
    achievements.interact(InvokeBehavior(user_id, command))

  if response is None:
    response = "Unknown command! Try `!help` for supported commands."

  if ephemeral:
    client.api_call("chat.postEphemeral", channel=channel_id, text=response, user=user_id)
  else:
    client.api_call("chat.postMessage", channel=channel_id, text=response)

def scheduled_actions():
  """Execute actions at scheduled times."""
  state = State.get()
  channel_id = state.channel_id()

  # Check if any obtained achievements should be broadcast.
  achievements = Achievements.get()
  for (user_id, text) in achievements.scheduled_broadcasts():
    response = ":bell: <@{}> obtained achievement: *{}*".format(user_id, text)
    client.api_call("chat.postMessage", channel=channel_id, text=response)

  # Ignore on saturdays and sundays.
  now = datetime.today()
  if now.weekday() >= 5:
    return

  # Morning announcement for participants to join game.
  start = datetime.combine(date.today(), MORNING_ANNOUNCE)
  end = start + MORNING_ANNOUNCE_DELTA
  if now >= start and now < end and not state.morning_announce():
    announce_text = "<!channel> Remember to join today's game before 11:50 by using" \
      " `!join` or :+1: reaction to this message!"

    resp = client.api_call("chat.postMessage", channel=channel_id, text=announce_text)
    state.set_morning_announce(resp["ts"])

    # First of the month (or closest monday) announcement for season reset
    month = calendar.month_name[datetime.today().month]
    if now.day == 1 or (now.weekday() == 0 and now.day <= 3):
      season_start_text = ":stadium: *{} season starts today!*\n".format(month)
      season_start_text += ":trophy: Previous season achievements have been calculated.\n"
      season_start_text += ":bar_chart: Stats and leaderboards shown with `!stats` will only " \
        "include the current season.\n"
      season_start_text += ":globe_with_meridians: Use `!allstats` for full statistics.\n"
      # TODO: Display fun facts about the season

      stats = Stats.get()
      stats.generate()
      players = stats.get_personals()
      for p in players:
        achievements.interact(SeasonStartBehavior(p))

      client.api_call("chat.postMessage", channel=channel_id, text=season_start_text)

    # Last of the month (or closest friday) warning for season reset
    month_range = calendar.monthrange(now.year, now.month)
    if now.day == month_range[1] or (now.weekday() == 4 and (month_range[1] - now.day <= 2)):
      season_end_text = ":rotating_light: *Last day of the {} season!* "\
        ":rotating_light:\n".format(month)
      season_end_text += ":chart_with_upwards_trend: Last chance to affect the season " \
          "rankings and gain achievements!"
      client.api_call("chat.postMessage", channel=channel_id, text=season_end_text)

    state.save()

  # Reminder announcement for remaining participants to join game. But don't send to users that
  # explicitly didn't want to play today's game.
  start = datetime.combine(date.today(), REMINDER_ANNOUNCE)
  end = start + REMINDER_ANNOUNCE_DELTA
  if now >= start and now < end and not state.reminder_announce():
    scores = Scores.get()
    remaining = scores.recent_users(7) - set(state.participants()) - set(state.dont_remind_users())
    if len(remaining) == 0:
      print("No one to remind!")
      # Something that won't match timestamp but still isn't None.
      state.set_reminder_announce(1)
    else:
      fmt = ", ".join(["<@{}>".format(uid) for uid in remaining])
      text = "{} Remember to join today's game before 11:50 by using `!join` or :+1: " \
        "reaction to this message!".format(fmt)
      resp = client.api_call("chat.postMessage", channel=channel_id, text=text)
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

  # Clear state at night, right before next day begins.
  start = datetime.combine(date.today(), NIGHT_CLEARING)
  end = start + NIGHT_CLEARING_DELTA
  should_clear = (len(state.participants()) > 0 or len(state.teams()) > 0 or
                  len(state.teams()) > 0 or len(state.team_names()) > 0 or
                  len(state.dont_remind_users()) > 0)
  if now >= start and now < end and should_clear:
    print("Executing nightly cleanup")
    state.set_schedule([])
    state.set_teams([])
    state.set_team_names([])
    state.set_unrecorded_matches([])
    state.set_participants([])
    state.set_dont_remind_users([])
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
  Scores.get()
  Stats.get()
  Achievements.get()

  if len(config.privileged_users()) == 0:
    print("No privileged users defined in config!")

  if not DEMO and state.bot_id() is None:
    state.set_bot_id(client.api_call("auth.test")["user_id"])
  print("Tourney bot ID: {}".format(state.bot_id()))

  # Find the channel ID of designated channel name.
  if not DEMO and state.channel_id() is None:
    channel_id = lookup.channel_id_by_name(CHANNEL_NAME)
    if channel_id is None:
      print("Could not find ID for channel: {}".format(CHANNEL_NAME))
      exit(1)
    state.set_channel_id(channel_id)
  print("#{} channel ID: {}".format(CHANNEL_NAME, state.channel_id()))

  state.save()

  # Send message channel that the bot has been started. This also makes it visible if the bot
  # suddenly restarts etc.
  git_describe = \
    subprocess.check_output(["git", "describe", "--all", "--long"], cwd=os.getcwd())  # nosec
  git_describe = git_describe.strip().decode("utf-8")
  started_text = "My engines have just been fired up! [{}]".format(git_describe)
  client.api_call("chat.postMessage", channel=state.channel_id(), text=started_text)

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
  if DEMO:
    print("=== Running in demo mode! ===")
  else:
    if not bot_token:
      print("TOURNEY_BOT_TOKEN must be defined in environment!")
      exit(1)
    connect()

  init()

  if LOAD_TEST:
    print("Exiting load test.")
    exit(0)

  repl()
