import os
import re
import itertools
import subprocess
from time import sleep
from datetime import datetime, date
from random import shuffle
from slackclient import SlackClient

from .command import Command
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

def parse_events(events):
  for event in events:
    event_type = event["type"]

    # Handle commands.
    if event_type == "message" and not "subtype" in event:
      msg = event["text"].strip()
      user_id = event["user"]

      cmd = Command.parse(event)
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
  response = None
  user_id = cmd.user_id
  user_name = lookup.user_name_by_id(user_id)
  command = cmd.command
  ephemeral = True
  state = State.get()
  channel_id = cmd.channel
  if not channel_id:
    channel_id = state.channel_id()
  participants = state.participants()

  if not cmd.allowed():
    response = "`!{}` is a privileged command and you're not allowed to use it!".format(command)

  elif command == "help":
    response = """
As the foosball bot, I accept the following commands:
  `!help` - Shows this text.
  `!list` - List users that joined game of the day.
  `!join` or positive reaction - Join game of the day.
  `!leave` or negative reaction - Leave game of the day.
  `!win` - Add match scores (irrelevant order) as a member of the winning team. Example: `!win 8 3`
  `!lose` - Add match scores (irrelevant order) as a member of the losing team. Example: `!lose 8 3`
  `!score` - Add match scores of two teams. Example: `!score T0 12 T3 16`
  `!stats` - Prints general statistics of all games.
  `!mystats` - Prints statistics of all games about invoker.
  `!undoteams` - Undoes teams and matches and restores as players joined. (*privileged!*)
  `!generate` - Generate teams and matches from players joined. (*privileged!*)
  `!autoupdate` - Updates project git repo and restarts bot. (*privileged!*)

Positive reactions: {}
Negative reactions: {}
""".format(" ".join([":{}:".format(r) for r in POSITIVE_REACTIONS]),
           " ".join([":{}:".format(r) for r in NEGATIVE_REACTIONS]))
  elif command == "list":
    ephemeral = False
    amount = len(participants)
    if amount == 0:
      response = "No players have joined yet!"
    else:
      response = "List of {} players for game of the day:".format(amount)
      for uid in participants:
        name = lookup.user_name_by_id(uid)
        response += "\n\t{}".format(name)
    if amount < 4:
      response += "\nAt least 4 players are required to create matches."
  elif command == "join":
    if user_id not in participants:
      state.add_participant(user_id)
      state.save()
      response = "{}, you've joined today's game!".format(user_name)
    else:
      response = "{}, you've _already_ joined today's game!".format(user_name)
  elif command == "leave":
    if user_id not in participants:
      response = "{}, you've _not_ joined today's game!".format(user_name)
    else:
      state.remove_participant(user_id)
      state.save()
      response = "{}, you've left today's game!".format(user_name)
  elif command == "score":
    ephemeral = False
    channel_id = state.channel_id()
    teams = state.teams()
    names = state.team_names()
    unrecorded_matches = state.unrecorded_matches()
    if len(teams) == 0:
      response = "Cannot report scores when no teams have been created!"
    else:
      example = "`!score T0 12 T3 16`"
      m = re.match(SCORE_ARGS_REGEX, cmd.args)
      if not m:
        response = "Requires arguments for teams and scores! Like {}".format(example)
      else:
        team_a = int(m.group(1)[1:])
        team_a_score = int(m.group(2))
        team_a_name = names[team_a]
        team_b = int(m.group(3)[1:])
        team_b_score = int(m.group(4))
        team_b_name = names[team_b]
        r = range(len(teams))
        if team_a in r and team_b in r and team_a_score >= 0 and team_b_score >= 0 and \
           (team_a_score % 8 == 0 or team_b_score % 8 == 0):
          key = [team_a, team_b]
          key.sort()
          if key in unrecorded_matches:
            ids_a = teams[team_a]
            ids_b = teams[team_b]
            if user_id in ids_a or user_id in ids_b:
              unrecorded_matches.remove(key)
              state.set_unrecorded_matches(unrecorded_matches)
              state.save()
              scores = Scores.get()
              scores.add(ids_a, team_a_score, ids_b, team_b_score)
              scores.save()
              response = "Added scores for [T{}] *{}* ({} pts) v [T{}] *{}* ({} pts)!".\
                format(team_a, team_a_name, team_a_score, team_b, team_b_name, team_b_score)
              rem = len(unrecorded_matches)
              if rem == 0:
                response += "\nNo more matches left to record!"
                handle_command(Command(user_id, "stats"))
              else:
                response += "\n{} matches left to record!".format(rem)
            else:
              response = "Only players of a match can report the score!"
          else:
            response = "Match has already been recorded or isn't scheduled!"
        else:
          response = """
Invalid arguments!
Teams must be input like 'T1' and scores must be positive and one be divisible by 8.
Example: {}
""".format(example)
  elif command == "win" or command == "lose":
    win = command == "win"
    ephemeral = False
    channel_id = state.channel_id()
    teams = state.teams()
    names = state.team_names()
    unrecorded_matches = state.unrecorded_matches()
    if len(teams) == 0:
      response = "Cannot report scores when no teams have been created!"
    else:
      example = "`!{} 12 16`".format(command)
      m = re.match(WIN_ARGS_REGEX, cmd.args)
      if not m:
        response = "Requires arguments for scores! Like {}".format(example)
      else:
        scores = list(map((int), m.groups()))
        winIndex = scores.index(max(scores))
        loseIndex = scores.index(min(scores))
        if win:
          myScore = scores[winIndex]
          theirScore = scores[loseIndex]
        else:
          myScore = scores[loseIndex]
          theirScore = scores[winIndex]
        if (myScore >= 0 and theirScore >= 0) and (myScore % 8 == 0 or theirScore % 8 == 0):
          myTeams = [x for x in teams if user_id in x]
          if len(myTeams) == 1:
            myTeam = myTeams[0]
            myTeamIndex = teams.index(myTeam)
            myTeamName = names[myTeamIndex]
            myMatches = [x for x in unrecorded_matches if myTeamIndex in x]
            if len(myMatches) == 1:
              myMatch = myMatches[0]
              theirTeamIndex = myMatch[(myMatch.index(myTeamIndex)+1)%2]
              theirTeam = teams[theirTeamIndex]
              theirTeamName = names[theirTeamIndex]

              unrecorded_matches.remove(myMatch)
              state.set_unrecorded_matches(unrecorded_matches)
              state.save()
              scores = Scores.get()
              scores.add(myTeam, myScore, theirTeam, theirScore)
              scores.save()
              response = "Added scores for [T{}] *{}* ({} pts) v [T{}] *{}* ({} pts)!".\
                format(myTeamIndex, myTeamName, myScore, theirTeamIndex, theirTeamName, theirScore)
              rem = len(unrecorded_matches)
              if rem == 0:
                response += "\nNo more matches left to record!"
                handle_command(Command(user_id, "stats"))
              else:
                response += "\n{} matches left to record!".format(rem)
            elif len(myMatches) > 1:
              response = "You appear in multiple matches. Please use explicit scoring with !score."
            else:
              response = "Found no unscored matches with you as a player."
          else:
            response = "You do not appear in any teams."
        else:
          response = "Scores must be positive and one be divisible by 8."
  elif command == "stats":
    ephemeral = False
    stats = Stats.get()
    if not stats.generate():
      response = "There are no recorded matches to generate statistics from!"
    else:
      stats.save()
      response = stats.general_response(lookup)
  elif command == "mystats":
    stats = Stats.get()
    if not stats.generate():
      response = "There are no recorded matches to generate statistics from!"
    else:
      stats.save()
      response = stats.personal_response(lookup, user_id)
  elif command == "undoteams":
    ephemeral = False

    if len(state.teams()) == 0:
      response = "No teams and matches to dissolve!"
    else:
      # Flatten teams lists.
      state.set_participants(list(itertools.chain.from_iterable(state.teams())))

      state.set_teams([])
      state.set_team_names([])
      state.set_unrecorded_matches([])
      state.set_midday_announce(False)
      state.save()
      response = \
        "Games have been canceled, teams dissolved, and all players are on the market again!"
  elif command == "generate":
    create_matches()
    return
  elif command == "autoupdate":
    subprocess.Popen(["/bin/sh", "autoupdate.sh"])
    exit(0)

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
