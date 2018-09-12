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
      rounds = 0
      total_score = 0
      avg_delta = 0
      player_matches = {}
      player_rounds = {}
      player_scores = {}
      player_wins = {}
      teams = {}

      def player_score_count(team, score):
        for player in team:
          if not player in player_scores:
            player_scores[player] = 0
          player_scores[player] += score
          if not player in player_matches:
            player_matches[player] = 0
          player_matches[player] += 1

      def team_win_count(team_key, team, win_team, match_rounds):
        if not team_key in teams:
          teams[team_key] = (0, 0)
        t = teams[team_key]
        teams[team_key] = (t[0] + (match_rounds if team == win_team else 0), t[1] + match_rounds)

      for match in matches:
        team_a = match[1]
        team_a.sort()
        team_a_key = ",".join(team_a) # lists/sets aren't hashable so turn into string.
        score_a = match[2]
        team_b = match[3]
        team_b.sort()
        team_b_key = ",".join(team_b) # Make hashable.
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

        # Count rounds won.
        match_rounds = (win_score // 8)
        rounds += match_rounds

        # Count rounds and wins for team configurations.
        team_win_count(team_a_key, team_a, win_team, match_rounds)
        team_win_count(team_b_key, team_b, win_team, match_rounds)

        for player in win_team:
          if player not in player_wins:
            player_wins[player] = 0
          player_wins[player] += match_rounds
        for player in team_a + team_b:
          if player not in player_rounds:
            player_rounds[player] = 0
          player_rounds[player] += match_rounds

      self.__rounds = rounds
      self.__team_amount = len(teams)
      self.__total_score = total_score
      self.__avg_score = total_score / amount
      self.__avg_delta = avg_delta / amount

      # Average all players' total scores and won rounds by the amount of rounds they played.
      for player in player_scores:
        player_scores[player] /= player_rounds[player]
      for player in player_wins:
        player_wins[player] = player_wins[player] / player_rounds[player] * 100.0

      # Substitute all team wins with the ratio of winning compared to rounds played.
      for team in teams:
        res = teams[team]
        teams[team] = (res[0] / res[1], res[1])

      def to_list(dict):
        ranking = [(p, dict[p]) for p in dict]
        return ranking

      # Sort players/teams with greatest scores and wins first, and a secondary factor. Make every
      # nudge factor only count a 1/1000th.
      self.__top_scorers = to_list(player_scores)
      self.__top_scorers.sort(key=lambda pair: pair[1] + player_wins[pair[0]]/10000, reverse=True)

      self.__top_winners = to_list(player_wins)
      self.__top_winners.sort(key=lambda pair: pair[1] + player_scores[pair[0]]/800, reverse=True)

      def teams_key(pair):
        scores = [player_scores[p] for p in pair[0].split(",")]
        avg_score = sum(scores) / len(scores)
        return avg_score / 800 + pair[1][0]

      self.__top_teams = to_list(teams)
      self.__top_teams.sort(key=teams_key, reverse=True)

      # Substitute top team string representations with list: "p1,p2" -> ["p1", "p2"]
      for i in range(len(self.__top_teams)):
        team = self.__top_teams[i]
        self.__top_teams[i] = (team[0].split(","), team[1])

      # Personal player info.
      for player in player_matches:
        info = {
          "total_matches": player_matches[player],
          "total_rounds": player_rounds[player],
          "total_score": player_scores[player],
          "total_wins": player_wins[player],
        }
        self.__personal[player] = info
    return True

  def general_response(self, lookup):
    top_amount = 5
    team_amount = 10
    return """
Total matches: {}
Total rounds: {}
Total teams: {}
Total score: {}
Average score: {:.2f}
Average delta: {:.2f}
Top {} players (avg score / round): {}
Top {} players (% of rounds won): {}
Top {} teams (% of rounds won): {}
""".format(self.__matches, self.__rounds, self.__team_amount, self.__total_score, \
           self.__avg_score, self.__avg_delta, top_amount, \
           self.__fmt_top(self.__top_scorers, top_amount, lookup), top_amount, \
           self.__fmt_top(self.__top_winners, top_amount, lookup), team_amount, \
           self.__fmt_top_teams(self.__top_teams, team_amount, lookup))

  def personal_response(self, lookup, user_id):
    if not user_id in self.__personal:
      return "No personal statistics recorded yet!"
    stats = self.__personal[user_id]
    rounds = stats["total_rounds"]
    win_perc = stats["total_wins"]
    win_rounds = int(win_perc * rounds / 100.0)
    teams = []
    for team in self.__top_teams:
      if user_id in team[0]:
        teams.append(team)
    return """
You scored {:.2f} goals on average in {} matches ({} rounds),
and won {:.2f}% ({} rounds)!
You have been in {} teams: {}
""".format(stats["total_score"], stats["total_matches"], rounds, win_perc, win_rounds, len(teams), \
           self.__fmt_top_teams(teams, len(teams), lookup))

  def file_path(self):
    return os.path.expanduser("{}/stats.json".format(DATA_PATH))

  def reset(self):
    self.__matches = 0
    self.__rounds = 0
    self.__team_amount = 0
    self.__total_score = 0
    self.__avg_score = 0.0
    self.__avg_delta = 0.0
    self.__top_scorers = []
    self.__top_winners = []
    self.__top_teams = []
    self.__personal = {}

  def save(self):
    data = {
      "matches": self.__matches,
      "rounds": self.__rounds,
      "team_amount": self.__team_amount,
      "total_score": self.__total_score,
      "avg_score": self.__avg_score,
      "avg_delta": self.__avg_delta,
      "top_scorers": self.__top_scorers,
      "top_winners": self.__top_winners,
      "top_teams": self.__top_teams,
      "personal": self.__personal
    }
    os.makedirs(os.path.dirname(self.file_path()), exist_ok=True)
    with open(self.file_path(), "w+") as fp:
      json.dump(data, fp, indent=2)

  def load(self):
    with open(self.file_path(), "r") as fp:
      data = json.load(fp)
      if "matches" in data:
        self.__matches = data["matches"]
      if "rounds" in data:
        self.__rounds = data["rounds"]
      if "team_amount" in data:
        self.__team_amount = data["team_amount"]
      if "total_score" in data:
        self.__total_score = data["total_score"]
      if "avg_score" in data:
        self.__avg_score = data["avg_score"]
      if "avg_delta" in data:
        self.__avg_delta = data["avg_delta"]
      if "top_scorers" in data:
        self.__top_scorers = data["top_scorers"]
      if "top_winners" in data:
        self.__top_winners = data["top_winners"]
      if "top_teams" in data:
        self.__top_teams = data["top_teams"]
      if "personal" in data:
        self.__personal = data["personal"]

  def __fmt_num(self, num):
    if isinstance(num, float):
      return "{:.2f}".format(num)
    return "{}".format(num)

  def __fmt_top(self, lst, amount, lookup):
    """Expects that `self.__personal` has already been filled!"""
    res = ""
    i = 0
    medals = ["first_place_medal", "second_place_medal", "third_place_medal"]
    for player in lst[0:amount]:
      name = lookup.user_name_by_id(player[0])
      num = self.__fmt_num(player[1])
      rounds = self.__personal[player[0]]["total_rounds"]
      medal = ""
      if i < 3:
        medal = ":{}: ".format(medals[i])
      res += "\n\t{}{}: {} ({} rounds)".format(medal, name, num, rounds)
      i += 1
    return res

  def __fmt_top_teams(self, lst, amount, lookup):
    res = ""
    i = 0
    medals = ["first_place_medal", "second_place_medal", "third_place_medal"]
    for team in lst[0:amount]:
      names = ", ".join([lookup.user_name_by_id(uid) for uid in team[0]])
      win_ratio = self.__fmt_num(team[1][0] * 100.0)
      rounds = team[1][1]
      medal = ""
      if i < 3:
        medal = ":{}: ".format(medals[i])
      res += "\n\t{}{}: {} ({} rounds)".format(medal, names, win_ratio, rounds)
      i += 1
    return res
