import os
import json

import itertools
from random import choice, shuffle

from .constants import DATA_PATH

class Teams:
  __instance = None

  def __init__(self):
    if not Teams.__instance:
      self.reset()

      try:
        self.load()
      except Exception as ex:
        print("Teams file could not load: {}".format(self.file_path()))
        print(ex)

      # Save default teams file if it doesn't exist.
      if not os.path.exists(self.file_path()):
        print("Saving empty teams: {}".format(self.file_path()))
        self.save()

      Teams.__instance = self

  @staticmethod
  def get():
    if not Teams.__instance:
      return Teams()
    return Teams.__instance

  def get_regenerated_users(self):
    return (self.__regenerated_2p_users, self.__regenerated_3p_users)

  def split_teams(self, n):
    if n in (1, 0):
      return []
    elif n == 2:
      return [1, 1]
    elif n == 3:
      return [1, 1, 1]
    elif n == 7:
      return [2, 2, 3]
    else:
      remainder = n % 4
      num_teams = (n - remainder) // 2
      duos = [2] * (num_teams - remainder)
      trios = [3] * remainder
      return duos + trios

  def get_teams_for_players(self, current_players):
    self.__regenerated_2p_users = []
    self.__regenerated_3p_users = []
    # Add any new players to data and generate their pairings
    self.__set_players(current_players)

    player_amount = len(current_players)
    if player_amount == 1:
      return None

    # Get valid teams
    valid_teams = {}
    valid_teams[2] = [t for t in self.__get_teams_2p() if
                      all(p in current_players for p in t)]
    valid_teams[3] = [t for t in self.__get_teams_3p() if
                      all(p in current_players for p in t)]

    teams = []

    team_player_numbers = self.split_teams(player_amount)
    for team_player_number in team_player_numbers:
      team = []
      if team_player_number == 1:
        p1 = choice(current_players)  # nosec
        team = [p1]
        current_players.remove(p1)
      else:
        valid_teams_for_count = valid_teams[team_player_number]

        if len(valid_teams_for_count) == 0:
          # Ran out of teams, generate for the remaining players
          for user_id in current_players:
            if team_player_number == 2:
              self.__generate_2p_teams_for_player(user_id)
              valid_teams[2] = [t for t in self.__get_teams_2p() if
                                all(p in current_players for p in t)]
            else:
              self.__generate_3p_teams_for_player(user_id)
              valid_teams[3] = [t for t in self.__get_teams_3p() if
                                all(p in current_players for p in t)]
          valid_teams_for_count = valid_teams[team_player_number]

        team = choice(valid_teams_for_count)  # nosec

        if team_player_number == 2:
          self.__teams_2p.remove(team)
        else:
          self.__teams_3p.remove(team)

        for user_id in team:
          # Remove other teams with players
          valid_teams[2] = [t for t in valid_teams[2] if user_id not in t]
          valid_teams[3] = [t for t in valid_teams[3] if user_id not in t]
          current_players.remove(user_id)

      teams.append(list(team))

    shuffle(teams)  # nosec

    self.save()

    return teams

  def __generate_2p_teams_for_player(self, user_id):
    self.__regenerated_2p_users.append(user_id)

    self.__teams_2p = {t for t in self.__teams_2p if user_id not in t}

    teams = []
    others = [p for p in self.__players if p != user_id]
    for player in others:
      new_team = tuple(sorted((user_id, player)))
      self.__teams_2p.add(new_team)
      teams.append(new_team)
    return teams

  def __generate_3p_teams_for_player(self, user_id):
    self.__regenerated_3p_users.append(user_id)

    self.__teams_3p = {t for t in self.__teams_3p if user_id not in t}

    teams = []
    others = [p for p in self.__players if p != user_id]
    all_2p_teams = itertools.combinations(others, 2)
    for t2p in all_2p_teams:
      new_team = tuple(sorted((user_id, t2p[0], t2p[1])))
      self.__teams_3p.add(new_team)
      teams.append(new_team)
    return teams

  def __set_players(self, players):
    # Generate teams for added players
    new_players = [p for p in players if p not in self.__players]
    for new_player in new_players:
      self.__generate_2p_teams_for_player(new_player)
      self.__generate_3p_teams_for_player(new_player)
      self.__players.add(new_player)

  def __get_teams_2p(self):
    if not self.__teams_2p:
      for p in self.__players:
        self.__generate_2p_teams_for_player(p)
    return self.__teams_2p

  def __get_teams_3p(self):
    if not self.__teams_3p:
      for p in self.__players:
        self.__generate_3p_teams_for_player(p)
    return self.__teams_3p

  def file_path(self):
    return os.path.expanduser("{}/teams.json".format(DATA_PATH))

  def reset(self):
    self.__teams_2p = set()
    self.__teams_3p = set()
    self.__players = set()

  def save(self):
    data = {
      "players": list(self.__players),
      "teams_2p": list(self.__get_teams_2p()),
      "teams_3p": list(self.__get_teams_3p())
    }
    os.makedirs(os.path.dirname(self.file_path()), exist_ok=True)
    with open(self.file_path(), "w+", encoding="utf-8") as fp:
      json.dump(data, fp, indent=2)

  def load(self):
    with open(self.file_path(), "r", encoding="utf-8") as fp:
      data = json.load(fp)
      if "players" in data:
        self.__players = set(data["players"])
      if "teams_2p" in data:
        teams_2p = data["teams_2p"]
        for t in teams_2p:
          self.__teams_2p.add(tuple(sorted(t)))
      if "teams_3p" in data:
        teams_3p = data["teams_3p"]
        for t in teams_3p:
          self.__teams_3p.add(tuple(sorted(t)))
