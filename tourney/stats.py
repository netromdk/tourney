import os
import json

from .constants import DATA_PATH
from .scores import Scores

class Stats:
  __instance = None

  def __init__(self):
    if not Stats.__instance:
      self.reset()

      try:
        self.load()
      except Exception as ex:
        print("Stats file could not load: {}".format(self.file_path()))
        print(ex)

      Stats.__instance = self

  @staticmethod
  def get():
    if not Stats.__instance:
      return Stats()
    return Stats.__instance

  def generate(self):
    self.reset()
    scores = Scores.get()
    matches = scores.matches()
    amount = len(matches)
    self.__matches = amount
    if amount == 0:
      return False
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
        win_score = score_a
        if score_b > score_a:
          win_team = team_b
          win_score = score_b
        for player in win_team:
          if player not in player_wins:
            player_wins[player] = 0
          # Count rounds won.
          player_wins[player] += (win_score // 8)

      self.__total_score = total_score
      self.__avg_score = total_score / amount
      self.__avg_delta = avg_delta / amount

      def sort(dict, amount):
        ranking = [(p, dict[p]) for p in dict]
        ranking.sort(key=lambda pair: pair[1], reverse=True)
        return ranking[0:amount]

      # Sort player scores and wins greatest first.
      self.__top_amount = 5
      self.__top_scorers = sort(player_scores, self.__top_amount)
      self.__top_winners = sort(player_wins, self.__top_amount)
    return True

  def general_response(self, lookup):
    return """
Total matches: {}
Total score: {}
Average score: {:.2f}
Average delta: {:.2f}
Top {} players (by score): {}
Top {} players (by rounds won): {}
""".format(self.__matches, self.__total_score, self.__avg_score, self.__avg_delta, \
           self.__top_amount, self.__fmt_top(self.__top_scorers, lookup), self.__top_amount, \
           self.__fmt_top(self.__top_winners, lookup))

  def file_path(self):
    return os.path.expanduser("{}/stats.json".format(DATA_PATH))

  def reset(self):
    self.__matches = 0
    self.__total_score = 0
    self.__avg_score = 0.0
    self.__avg_delta = 0.0
    self.__top_amount = 5
    self.__top_scorers = []
    self.__top_winners = []

  def save(self):
    data = {
      "matches": self.__matches,
      "total_score": self.__total_score,
      "avg_score": self.__avg_score,
      "avg_delta": self.__avg_delta,
      "top_amount": self.__top_amount,
      "top_scorers": self.__top_scorers,
      "top_winners": self.__top_winners,
    }
    os.makedirs(os.path.dirname(self.file_path()), exist_ok=True)
    with open(self.file_path(), "w+") as fp:
      json.dump(data, fp, indent=2)

  def load(self):
    with open(self.file_path(), "r") as fp:
      data = json.load(fp)
      if "matches" in data:
        self.__matches = data["matches"]
      if "total_score" in data:
        self.__total_score = data["total_score"]
      if "avg_score" in data:
        self.__avg_score = data["avg_score"]
      if "avg_delta" in data:
        self.__avg_delta = data["avg_delta"]
      if "top_amount" in data:
        self.__top_amount = data["top_amount"]
      if "top_scorers" in data:
        self.__top_scorers = data["top_scorers"]
      if "top_winners" in data:
        self.__top_winners = data["top_winners"]

  def __fmt_top(self, lst, lookup):
    return "\n\t" + \
      "\n\t".join(["{} ({})".format(lookup.user_name_by_id(p[0]), p[1]) for p in lst])

