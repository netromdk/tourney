from .constants import PRIVILEGED_COMMANDS
from .config import Config
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

def last_season_filter(match_stamp):
  today = date.today()
  match = datetime.fromtimestamp(match_stamp)
  if today.month == 1:
    return match.month == 12 and match.year == today.year - 1
  else:
    return match.month == today.month - 1 and match.year == today.year

def to_ordinal(number):
  suffixes = ['{}th', '{}st', '{}nd', '{}rd']
  if number >= 10 and number <= 20:
    suffix = '{}th'
  elif number % 10 in range(1, 4):
    suffix = suffixes[number % 10]
  else:
    suffix = '{}th'
  return suffix.format(number)
