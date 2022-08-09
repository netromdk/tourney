import os
import json
from datetime import datetime

from .constants import DATA_PATH, MEDAL_LIST
from .scores import Scores
from .util import fmt_duration, to_ordinal

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

  def generate(self, time_back_delta=None, time_filter=None):
    self.reset()
    scores = Scores.get()
    matches = scores.matches()
    self.__matches = 0
    if len(matches) == 0:
      return False

    rounds = 0
    total_score = 0
    avg_delta = 0
    player_matches = {}
    player_rounds = {}
    player_scores = {}
    player_wins = {}
    teams = {}
    oldest_time = None
    newest_time = None

    def player_score_count(team, score):
      for player in team:
        if player not in player_scores:
          player_scores[player] = 0
        player_scores[player] += score
        if player not in player_matches:
          player_matches[player] = 0
        player_matches[player] += 1

    def team_win_count(team_key, team, win_team, match_rounds):
      if team_key not in teams:
        teams[team_key] = (0, 0)
      t = teams[team_key]
      teams[team_key] = (t[0] + (match_rounds if team == win_team else 0), t[1] + match_rounds)

    now = datetime.utcnow()
    for match in matches:
      match_time = match[0]
      if time_back_delta is not None and \
         (now - time_back_delta) >= datetime.fromtimestamp(match_time):
        continue
      if time_filter is not None and not time_filter(match_time):
        continue

      self.__matches += 1

      if oldest_time is None and newest_time is None:
        oldest_time = match_time
        newest_time = match_time
      elif match_time < oldest_time:
        oldest_time = match_time
      elif match_time > newest_time:
        newest_time = match_time

      team_a = match[1]
      team_a.sort()
      team_a_key = ",".join(team_a)  # lists/sets aren't hashable so turn into string.
      score_a = match[2]
      team_b = match[3]
      team_b.sort()
      team_b_key = ",".join(team_b)  # Make hashable.
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
    self.__avg_score = 0
    self.__avg_delta = 0
    if self.__matches > 0:
      self.__avg_score = total_score / self.__matches
      self.__avg_delta = avg_delta / self.__matches
    self.__oldest_score_time = oldest_time
    self.__newest_score_time = newest_time

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

    def top_scorers_cmp(pair):
      res = pair[1]
      if pair[0] in player_wins:
        res += player_wins[pair[0]] / 10000
      return res
    self.__top_scorers.sort(key=top_scorers_cmp, reverse=True)
    self.__top_winners = to_list(player_wins)

    def top_winners_cmp(pair):
      res = pair[1]
      if pair[0] in player_scores:
        res += player_scores[pair[0]] / 800
      return res

    self.__top_winners.sort(key=top_winners_cmp, reverse=True)

    def teams_key(pair):
      scores = [player_scores[p] for p in pair[0].split(",")]
      avg_score = sum(scores) / len(scores)
      return avg_score / 800 + pair[1][0]

    self.__top_teams = to_list(teams)
    self.__top_teams.sort(key=teams_key, reverse=True)

    # Substitute top team string representations with list: "p1,p2" -> ["p1", "p2"]
    for i in range(len(self.__top_teams)):  # pylint: disable=consider-using-enumerate
      team = self.__top_teams[i]
      self.__top_teams[i] = (team[0].split(","), team[1])

    # Personal player info.
    for player in player_matches:
      info = {
        "total_matches": player_matches[player] if player in player_matches else 0,
        "total_rounds": player_rounds[player] if player in player_rounds else 0,
        "total_score": player_scores[player] if player in player_scores else 0,
        "total_wins": player_wins[player] if player in player_wins else 0,
      }
      self.__personal[player] = info
    return True

  def general_response(self, lookup):
    top_amount = 5
    top_range = range(top_amount)
    team_amount = 10
    team_range = range(team_amount)
    if self.__newest_score_time is not None and self.__oldest_score_time is not None:
      total_dur = fmt_duration(self.__newest_score_time - self.__oldest_score_time)
    else:
      total_dur = 0
    qualifying_scorers = self.__qualifying_players(self.__top_scorers)
    top_players_score = self.__fmt_top(qualifying_scorers, top_range, lookup)
    qualifying_winners = self.__qualifying_players(self.__top_winners)
    top_players_rounds = self.__fmt_top(qualifying_winners, top_range, lookup)
    top_teams = self.__fmt_top_teams(self.__top_teams, team_range, lookup)
    return f"""
Total matches: {self.__matches}
Total rounds: {self.__rounds}
Total teams: {self.__team_amount}
Total score: {self.__total_score}
Total duration: {total_dur}
Average score: {self.__avg_score:.2f}
Average delta: {self.__avg_delta:.2f}
Top {top_amount} players (avg score / round): {top_players_score}
Top {top_amount} players (% of rounds won): {top_players_rounds}
Top {team_amount} teams (% of rounds won): {top_teams}
"""

  def personal_response(self, lookup, user_id):
    if user_id not in self.__personal:
      return "No personal statistics recorded yet!"
    stats = self.__personal[user_id]
    rounds = stats["total_rounds"]
    win_perc = stats["total_wins"]
    win_rounds = int(win_perc * rounds / 100.0)
    lose_perc = 100.0 - win_perc
    lose_rounds = rounds - win_rounds
    teams = []
    for team in self.__top_teams:
      if user_id in team[0]:
        teams.append(team)
    max_teams = min(5, len(teams))
    return """
You scored {:.2f} goals on average in {} matches ({} rounds),
won {:.2f}% ({} rounds),
and lost {:.2f}% ({} rounds).
You have been in {} teams: {}
""".format(stats["total_score"], stats["total_matches"], rounds, win_perc, win_rounds, lose_perc,
           lose_rounds, len(teams), self.__fmt_top_teams(teams, range(max_teams), lookup))

  def local_placement(self, user_id):
    top = self.__top_winners
    top_enum = enumerate(top)
    try:
      placement = next(i for i, v in top_enum if v[0] == user_id)
    except StopIteration:
      placement = None
    return placement

  def local_top_list(self, user_id, delta, lookup):
    response = ""
    top = self.__qualifying_players(self.__top_winners)
    top_enum = enumerate(top)
    try:
      placement = next(i for i, v in top_enum if v[0] == user_id)
    except StopIteration:
      placement = None
    if placement is not None:
      local_start_index = max(0, placement - delta)
      local_end_index = min(placement + delta, len(top))
      local_top_range = range(local_start_index, local_end_index + 1)
      response += "Your current position in the ongoing season:"
      if local_start_index > 0:
        response += "\n\t..."
      response += self.__fmt_top(top, local_top_range, lookup)
      if local_end_index < len(top) - 1:
        response += "\n\t..."
    return response

  def file_path(self):
    return os.path.expanduser("{}/stats.json".format(DATA_PATH))

  def reset(self):
    self.__matches = 0
    self.__rounds = 0
    self.__team_amount = 0
    self.__total_score = 0
    self.__avg_score = 0.0
    self.__avg_delta = 0.0
    self.__oldest_score_time = None
    self.__newest_score_time = None
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
      "oldest_score_time": self.__oldest_score_time,
      "newest_score_time": self.__newest_score_time,
      "top_scorers": self.__top_scorers,
      "top_winners": self.__top_winners,
      "top_teams": self.__top_teams,
      "personal": self.__personal
    }
    os.makedirs(os.path.dirname(self.file_path()), exist_ok=True)
    with open(self.file_path(), "w+", encoding="utf-8") as fp:
      json.dump(data, fp, indent=2)

  def load(self):
    with open(self.file_path(), "r", encoding="utf-8") as fp:
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
      if "oldest_score_time" in data:
        self.__oldest_score_time = data["oldest_score_time"]
      if "newest_score_time" in data:
        self.__newest_score_time = data["newest_score_time"]
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

  def __qualifying_players(self, players):
    if len(self.__personal.values()) == 0:
      return players
    req_plays = max([p["total_matches"] for p in self.__personal.values()]) / 4
    qualifying_players = [p for p in players if self.__personal[p[0]]["total_matches"] >= req_plays]
    return qualifying_players

  def __fmt_top(self, players, list_range, lookup):
    """Expects that `self.__personal` has already been filled!"""
    res = ""

    for index in list_range:
      if index >= len(players):
        break
      player = players[index]
      name = lookup.user_name_by_id(player[0])
      num = self.__fmt_num(player[1])
      rounds = self.__personal[player[0]]["total_rounds"]
      placement_str = "{} ".format(to_ordinal(index + 1))
      if index < 3:
        placement_str = ":{}: ".format(MEDAL_LIST[index])
      res += "\n\t{}{}: {} ({} rounds)".format(placement_str, name, num, rounds)
    return res

  def __fmt_top_teams(self, lst, team_range, lookup):
    res = ""
    for index in team_range:
      if index >= len(lst):
        break
      team = lst[index]
      names = ", ".join([lookup.user_name_by_id(uid) for uid in team[0]])
      win_ratio = self.__fmt_num(team[1][0] * 100.0)
      rounds = team[1][1]
      placement_str = "{} ".format(to_ordinal(index + 1))
      if index < 3:
        placement_str = ":{}: ".format(MEDAL_LIST[index])
      res += "\n\t{}{}: {} ({} rounds)".format(placement_str, names, win_ratio, rounds)
    return res

  def get_personals(self):
    return self.__personal

  def get_top_winners(self):
    return self.__top_winners
