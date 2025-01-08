from random import random
from .player_skill import PlayerSkill
from .constants import PREFERRED_ROUNDS, MATCHMAKING
from .state import State
from .teams import Teams
from .teamnames import Teamnames
from .teamname_generator import generate_teamnames
from .util import schedule_text

def create_teams():
  """Create teams and random team names."""
  participants = State.get().participants()

  teams = Teams.get().get_teams_for_players(participants)

  if not teams:
    return None, None

  teamnames = Teamnames.get()
  names = generate_teamnames(len(teams))
  for (i, team) in enumerate(teams):
    name = teamnames.teamname(team)
    if name:
      names[i] = name

  return teams, names

def all_team_combinations(teams):
  """Returns all combinations of pairs of teams"""
  if len(teams) < 2:
    yield []
    return
  if len(teams) == 3:
    # Only one combination possible here
    yield [(teams[0], teams[1], 1),
           (teams[1], teams[2], 1),
           (teams[0], teams[2], 1)]
    return
  if len(teams) % 2 == 1:
    # Handle odd length list. Make one XvXvX and (n-3)/2 pairs.
    # Combine each possible triple with each possible configuration of the other teams
    for (i, team_i) in enumerate(teams):
      i_remains = list(range(len(teams)))
      i_remains.remove(i)
      for j in i_remains:
        j_remains = list(i_remains)
        j_remains.remove(j)
        for k in j_remains:
          triple = [(team_i, teams[j], 1), (team_i, teams[k], 1), (teams[j], teams[k], 1)]
          remains = [t for t in teams if t not in [team_i, teams[j], teams[k]]]
          for result in all_team_combinations(remains):
            yield triple + result
  else:
    a = teams[0]
    for i in range(1, len(teams)):
      # Pick a pair for a one-round match and recurse on rest of list
      pair = (a, teams[i], PREFERRED_ROUNDS)
      for r in all_team_combinations(teams[1:i] + teams[i + 1:]):
        yield [pair] + r

def pskill_quality(match):
  player_skill = PlayerSkill.get()
  return player_skill.get_match_quality(match)

def create_schedule(teams, rand_matches):
  """Takes list of teams to schedule for."""
  matches = []
  if len(teams) == 2:
    # Just the one game today, let's make it a two-rounder
    matches = [(0, 1, 2)]
  elif not rand_matches:
    all_combinations = list(all_team_combinations(list(range(len(teams)))))
    qualities = []
    for c in all_combinations:
      quality = 1.0
      for m in c:
        match = [teams[t] for t in m if t in teams]
        if len(match) == len(m):
          quality = min(quality, pskill_quality(match))
      qualities.append(quality)

    best_index = qualities.index(max(qualities))
    matches = all_combinations[best_index]
  else:
    if len(teams) % 2 == 0:
      # Add one-round matches for random pairs of teams
      matches = [(i, i + 1, 2) for i in range(0, len(teams), 2)]
    else:
      twoRounders = len(teams) - 3
      if twoRounders > 0:
        matches = [(i, i + 1, 2) for i in range(0, twoRounders, 2)]
      # Add last 3 matches of 1 round each.
      i = twoRounders
      matches += [(i, i + 1, 1),
                  (i, i + 2, 1),
                  (i + 1, i + 2, 1)]
  return matches

def create_matches(lookup):
  state = State.get()
  response = "<!channel>\n"
  teams, names = create_teams()

  if teams is None:
    response += "No games possible! At least 2 players are required!"
  else:
    # Whether or not to do matchmaking or random matchups.
    if not MATCHMAKING:
      rand_matches = True
    else:
      # 50% chance of random. Range is [0.0, 1.0)
      rand_matches = random() < 0.5  # nosec

    sched = create_schedule(teams, rand_matches)
    unrecorded_matches = []
    for match in sched:
      key = [match[0], match[1]]
      key.sort()
      unrecorded_matches.append(key)

    # Remember teams and unrecorded matches but clear participants, morning announce, and users that
    # didn't want today's reminder.
    state.set_schedule(sched)
    state.set_teams(teams)
    state.set_team_names(names)
    state.set_unrecorded_matches(unrecorded_matches)

    if len(teams) > 3 and rand_matches:
      response += ":tractor::dash: {} :tractor::dash:\n\n".\
        format("Today's matchups brought to you by the RANDOM FACTOR TRACTOR")

    # Generate response for the channel.
    response += schedule_text(lookup)

    tteams = Teams.get()
    (gen2p, gen3p) = tteams.get_regenerated_users()
    regen_set = set(gen2p + gen3p)
    if len(regen_set) > 0:
      response += "\n\n:recycle: Regenerated teams for:\n"
      for p in regen_set:
        response += "  {}\n".format(lookup.user_name_by_id(p))

  # Clean state
  state.set_participants([])
  state.set_morning_announce(None)
  state.set_dont_remind_users([])
  state.save()

  return response
