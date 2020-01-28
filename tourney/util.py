from .constants import PRIVILEGED_COMMANDS
from .config import Config
from .state import State
from .scores import Scores
from .player_skill import PlayerSkill

from datetime import date, datetime

def fmt_duration(secs, show_ms=False):
  ms = 0
  if isinstance(secs, float):
    ms = int((secs - float(int(secs))) * 1000)
    secs = int(secs)

  res = []

  months = secs // (30 * 24 * 3600)
  secs &= 30 * 24 * 3600
  if months > 0:
    res.append("{}mo".format(months))

  days = secs // (24 * 3600)
  secs %= 24 * 3600
  if days > 0:
    res.append("{}d".format(days))

  def pad(n):
    return "{}{}".format("0" if n < 10 else "", n)

  hours = secs // 3600
  secs %= 3600
  mins = secs // 60
  secs %= 60
  res.append("{}:{}:{}".format(pad(hours), pad(mins), pad(secs)))

  if show_ms:
    res.append("{}ms".format(ms))

  return " ".join(res)

def command_allowed(cmd, user_id):
  if cmd in PRIVILEGED_COMMANDS:
    return user_id in Config.get().privileged_users()
  return True

def unescape_text(text):
  return text.replace("\\n", "\n").replace("\\t", "  ")

def this_season_filter(match_stamp):
  today = date.today()
  match = datetime.fromtimestamp(match_stamp)
  return match.month == today.month and match.year == today.year

def nth_last_season_filter(n):
  def season_filter(match_stamp):
    today = date.today()
    year = today.year
    month = today.month

    while month <= n:
      year = year - 1
      month = month + 12
    month = month - n

    match_time = datetime.fromtimestamp(match_stamp)
    return match_time.month == month and match_time.year == year
  return season_filter

def to_ordinal(number):
  suffixes = ['{}th', '{}st', '{}nd', '{}rd']
  if number >= 10 and number <= 20:
    suffix = '{}th'
  elif number % 10 in range(1, 4):
    suffix = suffixes[number % 10]
  else:
    suffix = '{}th'
  return suffix.format(number)

def schedule_text(lookup):
  state = State.get()
  sched = state.schedule()
  teams = state.teams()
  names = state.team_names()

  if len(sched) == 0:
    return "There is no schedule yet!"

  scores = Scores.get()
  played = scores.today()
  ps = PlayerSkill.get()

  def team_str(members):
    return ", ".join([lookup.user_name_by_id(uid) for uid in members])

  res = "Schedule:"
  for match in sched:
    plural = "s" if match[2] > 1 else ""
    name_a = names[match[0]]
    team_a = teams[match[0]]
    team_a_str = team_str(team_a)
    team_a_score = None
    name_b = names[match[1]]
    team_b = teams[match[1]]
    team_b_str = team_str(team_b)
    team_b_score = None

    quality = int(ps.get_match_quality([team_a, team_b]) * 100)

    # Check if match was already played.
    for pm in played:
      if (pm[1] == team_a or pm[1] == team_b) and (pm[3] == team_a or pm[3] == team_b):
        if pm[1] == team_a:
          team_a_score = pm[2]
          team_b_score = pm[4]
        else:
          team_a_score = pm[4]
          team_b_score = pm[2]
        break

    res += "\n\t[T{}] *{}*: {}".format(match[0], name_a, team_a_str)
    if team_a_score is not None:
      res += " *({} pts)*".format(team_a_score)

    res += " vs. [T{}] *{}*: {}".format(match[1], name_b, team_b_str)
    if team_b_score is not None:
      res += " *({} pts)*".format(team_b_score)

    res += " ({} round{}, {}% quality)".format(match[2], plural, quality)
  return res
