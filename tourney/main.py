import os
from time import sleep
import re
from datetime import datetime, date, timedelta
from random import shuffle
from slackclient import SlackClient

from .command import Command
from .state import State
from .lookup import Lookup
from .constants import *
from .scores import Scores

client = SlackClient(os.environ.get("TOURNEY_BOT_TOKEN"))
lookup = Lookup(client)

def create_teams():
  participants = State.get().participants()
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
  state = State.get()
  response = "<!channel>\n"
  teams = create_teams()
  unrecorded_matches = []
  if teams is None:
    response += "Could not create teams! There must be at least 4 participants!"
  else:
    response += "{} teams: ".format(len(teams))
    for i in range(len(teams)):
      fmt = ", ".join([lookup.user_name_by_id(uid) for uid in teams[i]])
      response += "\n\t*T{}*: {}".format(i, fmt)
    sched = create_schedule(len(teams))
    response += "\n\nSchedule:"
    for match in sched:
      plural = "s" if match[2] > 1 else ""
      response += "\n\t*T{}* vs. *T{}* ({} round{})".format(match[0], match[1], match[2], plural)
      key = [match[0], match[1]]
      key.sort()
      unrecorded_matches.append(key)

    # Remember teams and unrecorded matches but clear participants and morning announce.
    state.set_teams(teams)
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

      m = re.match(COMMAND_REGEX, msg)
      if m:
        handle_command(Command(user_id, m.group(1), m.group(2).strip()))
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
  channel_id = state.channel_id()
  participants = state.participants()

  if command.startswith("help"):
    response = """
As the foosball bot, I accept the following commands:
  `!help` - Shows this text.
  `!list` - List users that joined game of the day.
  `!join` or positive reaction - Join game of the day.
  `!leave` or negative reaction - Leave game of the day.
  `!score` - Add match scores of two teams. Example: `!score T0 12 T3 16`
  `!stats` - Prints general statistics of all games.

Positive reactions: {}
Negative reactions: {}
""".format(" ".join([":{}:".format(r) for r in POSITIVE_REACTIONS]),
           " ".join([":{}:".format(r) for r in NEGATIVE_REACTIONS]))
  elif command.startswith("list"):
    ephemeral = False
    amount = len(participants)
    if amount == 0:
      response = "No participants have joined yet!"
    else:
      response = "List of {} participants for game of the day:".format(amount)
      for uid in participants:
        name = lookup.user_name_by_id(uid)
        response += "\n\t{}".format(name)
    if amount < 4:
      response += "\nAt least 4 participants are required to create matches."
  elif command.startswith("join"):
    if user_id not in participants:
      state.add_participant(user_id)
      state.save()
      response = "{}, you've joined today's game!".format(user_name)
    else:
      response = "{}, you've _already_ joined today's game!".format(user_name)
  elif command.startswith("leave"):
    if user_id not in participants:
      response = "{}, you've _not_ joined today's game!".format(user_name)
    else:
      state.remove_participant(user_id)
      state.save()
      response = "{}, you've left today's game!".format(user_name)
  elif command.startswith("score"):
    teams = state.teams()
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
        team_b = int(m.group(3)[1:])
        team_b_score = int(m.group(4))
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
              response = "Added scores!"
            else:
              response = "Only participants of a match can report the score!"
          else:
            response = "Match has already been recorded!"
        else:
          response = """
Invalid arguments!
Teams must be input like 'T1' and scores must be positive and one be divisible by 8.
Example: {}
""".format(example)
  elif command.startswith("stats"):
    ephemeral = False
    scores = Scores.get()
    matches = scores.matches()
    amount = len(matches)
    if amount == 0:
      response = "There are no recorded matches!"
    else:
      total_score = 0
      avg_delta = 0
      player_scores = {}
      player_wins = {}

      def player_score_count(team, score):
        for player in team:
          if not player in player_scores:
            player_scores[player] = 0
          player_scores[player] += score

      for match in matches:
        team_a = match[1]
        score_a = match[2]
        team_b = match[3]
        score_b = match[4]
        total_score += score_a + score_b
        avg_delta += abs(score_a - score_b)
        player_score_count(team_a, score_a)
        player_score_count(team_b, score_b)
        win_team = team_a
        if score_b > score_a:
          win_team = team_b
        for player in win_team:
          if player not in player_wins:
            player_wins[player] = 0
          player_wins[player] += 1
      avg_score = total_score / amount
      avg_delta /= amount

      def sort_and_format(dict, amount):
        ranking = [(p, dict[p]) for p in dict]
        ranking.sort(key=lambda pair: pair[1], reverse=True)
        subset = ranking[0:amount]
        return "\n\t" + \
          "\n\t".join(["{} ({})".format(lookup.user_name_by_id(p[0]), p[1]) for p in subset])

      # Sort player scores and wins greatest first.
      top_amount = 5
      top_players = sort_and_format(player_scores, top_amount)
      top_winners = sort_and_format(player_wins, top_amount)

      response = """
Total matches: {}
Total score: {}
Average score: {:.2f}
Average delta: {:.2f}
Top {} players (by score): {}
Top {} players (by wins): {}
""".format(amount, total_score, avg_score, avg_delta, top_amount, top_players, top_amount, \
           top_winners)

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
  end = start + timedelta(hours=1)
  if now >= start and now < end and not state.morning_announce():
    resp = client.api_call("chat.postMessage", channel=channel_id,
      text="<!channel> Remember to join today's game before 11:50 by using `!join` or :+1: "
           "reaction to this message!")
    state.set_morning_announce(resp["ts"])
    state.save()

  # Reminder announcement for remaining participants to join game.
  start = datetime.combine(date.today(), REMINDER_ANNOUNCE)
  end = start + timedelta(minutes=30)
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
  end = start + timedelta(minutes=10)
  if now >= start and now < end and not state.midday_announce():
    state.set_midday_announce(True)
    state.save()
    create_matches()
  elif now > end and state.midday_announce():
    print("Clearing midday announce")
    state.set_midday_announce(False)
    state.save()

def connect():
  if not client.rtm_connect(with_team_state=False):
    print("Could not connect to Slack!")
    exit(1)

  print("Connected!")

def init():
  state = State.get()
  scores = Scores.get()

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
