import os
import json
from calendar import monthrange
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num

from .constants import DATA_PATH

class Scores:
  __instance = None

  def __init__(self):
    if not Scores.__instance:
      self.reset()
      try:
        self.load()
      except Exception as ex:
        print("Scores file could not load: {}".format(self.file_path()))
        print(ex)

      Scores.__instance = self

  @staticmethod
  def get():
    if not Scores.__instance:
      return Scores()
    return Scores.__instance

  def add(self, first_team, first_score, second_team, second_score):
    """Add a match scores with each team being a list of slack user IDs."""
    self.__scores.append([
      datetime.utcnow().timestamp(),
      first_team,
      first_score,
      second_team,
      second_score
    ])

  def matches(self):
    return self.__scores

  def recent_users(self, last_days):
    """Returns active users within `last_days`."""
    past = datetime.utcnow() - timedelta(days=last_days)
    res = []
    for match in self.matches():
      if datetime.fromtimestamp(match[0]) >= past:
        for player in match[1] + match[3]:
          res.append(player)
    return set(res)

  def today(self):
    """List of results of today's matches, if any."""
    now = datetime.utcnow().date()
    res = []
    for match in self.matches():
      if datetime.fromtimestamp(match[0]).date() == now:
        res.append(match)
    return res

  def file_path(self):
    return os.path.expanduser("{}/scores.json".format(DATA_PATH))

  def reset(self):
    self.__scores = []

  def save(self):
    data = {
      "scores": self.__scores,
    }
    os.makedirs(os.path.dirname(self.file_path()), exist_ok=True)
    with open(self.file_path(), "w+") as fp:
      json.dump(data, fp)

  def load(self):
    with open(self.file_path(), "r") as fp:
      data = json.load(fp)
      if "scores" in data:
        self.__scores = data["scores"]

  def get_season_winrate_plot(self):
    pwins = {}

    monthscores = [x for x in self.__scores if
                   datetime.fromtimestamp(x[0]).month == datetime.now().month]
    monthscores.sort(key=lambda x: x[0])

    # Collect playername -> [(date, wins)]
    for score in monthscores:
      date = datetime.fromtimestamp(score[0])
      if score[2] > score[4]:
        winteam = score[1]
        loseteam = score[3]
      else:
        winteam = score[3]
        loseteam = score[1]
      for p in winteam:
        if p not in pwins:
          pwins[p] = [(date, 1)]
        else:
          wins = pwins[p][-1][1]
          pwins[p].append((date, wins + 1))
      for p in loseteam:
        if p not in pwins:
          pwins[p] = [(date, 0)]
        else:
          wins = pwins[p][-1][1]
          pwins[p].append((date, wins))

    fig, ax = plt.subplots()

    # Calc wins/matches for each player
    for p in pwins:
      dates = []
      pwinrate = []
      for i in range(len(pwins[p])):
        result = pwins[p][i]
        dates.append(date2num(result[0]))
        pwinrate.append(result[1] / (i + 1))
      ax.plot(dates, pwinrate, label=p)

    # round to nearest day
    now = datetime.now()
    datemin = now.replace(day=1)
    datemax = now.replace(day=monthrange(now.year, now.month)[1])
    ax.set_xlim(datemin, datemax)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

    plt.ylabel('Win percentage')
    plt.xlabel('Date')
    plt.gcf().autofmt_xdate()

    figure_filename = os.path.expanduser("{}/wingraph.png".format(DATA_PATH))
    plt.savefig(figure_filename)
    return figure_filename
