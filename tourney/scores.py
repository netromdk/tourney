import os
import json
from calendar import monthrange
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num
from matplotlib.ticker import FuncFormatter
import numpy as np

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

  def get_season_winrate_plot(self, lookup, time_filter=None):
    pwins = {}

    if time_filter:
      monthscores = [x for x in self.__scores if time_filter(x[0])]
    else:
      monthscores = [x for x in self.__scores if
                     datetime.fromtimestamp(x[0]).month == datetime.now().month]

    monthscores.sort(key=lambda x: x[0])

    # Get the highest number of matches a single person has played
    playcount = {}
    for score in monthscores:
      team1 = score[1]
      team2 = score[3]
      for p in team1 + team2:
        playcount[p] = playcount.setdefault(p, 0) + 1

    # required number of plays to figure in the graph
    req_plays = max(playcount.values()) / 4

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

    # Get playername -> [(sortable datestamps, win percentages)] for plotting
    p_winrates = {}
    for p, wins in pwins.items():
      if playcount[p] < req_plays:
        continue
      dates = []
      winrates = []
      for i in range(len(wins)):
        result = wins[i]
        dates.append(date2num(result[0]))
        winrates.append(result[1] / (i + 1))
      p_winrates[p] = (dates, winrates)

    # Stop if we don't have any win rates.
    if len(p_winrates) == 0:
      return None

    # Sort by final win percentage to mark the top 5
    p_sorted = sorted(p_winrates.keys(), key=lambda p: p_winrates[p][1][-1])
    p_sorted.reverse()

    # Add top 5 cutoff line
    p5 = p_sorted[4]
    p5_rate = p_winrates[p5][1][-1]

    ax.axhline(p5_rate, color='gold', lw=2)

    for i in range(len(p_sorted)):
      p = p_sorted[i]
      (dates, winrates) = p_winrates[p]
      if i < 5:
        pname = lookup.user_name_by_id(p)
        ax.plot(dates, winrates, label=pname, linewidth=3)
      else:
        ax.plot(dates, winrates, linewidth=1, linestyle="dashed", label='_nolegend_')

    # add legend lower right
    ax.legend(loc=4)

    # show whole month
    example_date = datetime.fromtimestamp(monthscores[0][0])
    datemin = example_date.replace(day=1)
    datemax = example_date.replace(day=monthrange(example_date.year, example_date.month)[1])
    ax.set_xlim(datemin, datemax)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))

    plt.ylabel('Win percentage')
    plt.xlabel('Date')
    plt.gcf().autofmt_xdate()

    figure_filename = os.path.expanduser("{}/wingraph.png".format(DATA_PATH))

    plt.savefig(figure_filename)
    return figure_filename

  def __get_scorigami_array(self):
    """Get number of times scored and last score date for each score.
       First array has one-rounders, second has two-rounders"""
    score_counts = [[(0, None) for i in range(16)], [(0, None) for i in range(16)]]

    for score in self.__scores:
      win_score = max(score[2], score[4])
      lose_score = min(score[2], score[4])
      if win_score == 16:
        win_index = 1
      else:
        win_index = 0

      score_date = datetime.fromtimestamp(score[0])

      (prev_count, prev_date) = score_counts[win_index][lose_score]

      if not prev_date or score_date > prev_date:
        score_counts[win_index][lose_score] = (prev_count + 1, score_date)
      else:
        score_counts[win_index][lose_score] = (prev_count + 1, prev_date)

    return score_counts

  def __heatmap(self, data, row_labels, col_labels, ax=None):
    if not ax:
      ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, cmap="Greens")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on bottom.
    ax.tick_params(top=False, bottom=True,
                   labeltop=False, labelbottom=True)

    # Turn spines off and create white grid.
    # for edge, spine in ax.spines.items():
    #   spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
    # ax.grid(which="minor", color="b", linestyle='-', linewidth=1)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im

  def __annotate_heatmap(self, im):
    data = im.get_array()

    threshold = im.norm(data.max()) / 2.
    textcolors = ["black", "white"]

    # Set default alignment to center
    kw = dict(horizontalalignment="center", verticalalignment="center", size=7)

    # Format as string to have "-" entries
    valfmt = matplotlib.ticker.StrMethodFormatter("{x:s}")

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
      for j in range(data.shape[1]):
        kw.update(color=textcolors[im.norm(data[i, j]) > threshold])
        if i == 0 and j >= 8:
          label = "-"
        else:
          label = "{}".format(data[i, j])
        text = im.axes.text(j, i, valfmt(label, None), **kw)
        texts.append(text)

    return texts

  def get_scorigami_plot(self):
    roundLabels = ["One round", "Two rounds"]
    goalLabels = list(range(0, 16))
    scorigami_array = self.__get_scorigami_array()

    scorigami_count_array = [[x[0] for x in scorigami_array[0]],
                             [x[0] for x in scorigami_array[1]]]
    np_scorigami_array = np.array(scorigami_count_array, dtype=int)

    fig, ax = plt.subplots()
    ax.set_title("Scorigami")

    im = self.__heatmap(np_scorigami_array, roundLabels, goalLabels, ax=ax)
    self.__annotate_heatmap(im)

    fig.tight_layout()

    figure_filename = os.path.expanduser("{}/scorigami.png".format(DATA_PATH))

    plt.savefig(figure_filename)
    return figure_filename

  def get_scorigami(self, win_score, lose_score):
    scorigami_array = self.__get_scorigami_array()
    if win_score == 16:
      win_index = 1
    else:
      win_index = 0
    scorigami = scorigami_array[win_index][lose_score]

    return scorigami
