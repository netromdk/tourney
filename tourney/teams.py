import os
import json

import itertools
from random import choice

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

  def get_teams_for_players(self, current_players):
    # Add any new players to data and generate their pairings
    self.__set_players(current_players)

    if len(current_players) == 1:
      return None
    elif len(current_players) == 2:
      return [[current_players[0]], [current_players[1]]]
    elif len(current_players) == 3:
      player_one = choice(current_players)  # nosec
      team_one = [player_one]
      team_two = (x for x in current_players if x != player_one)
      if team_two in self.__teams_2p:
        self.__teams_2p.remove(team_two)
      teams = [team_one, team_two]
      return teams

    # Get teams for the current player
    valid_2p_teams = []
    valid_3p_teams = []
    # Find all teams valid for the current lineup
    valid_2p_teams = [t for t in self.__get_teams_2p() if
                              all(p in current_players for p in t)]
    valid_3p_teams = [t for t in self.__get_teams_3p() if
                              all(p in current_players for p in t)]

    teams = []

    while current_players:
      user_id = current_players[0]
      # If a player is in no valid teams, generate new teams for them
      # 2p teams
      valid_2p_teams_for_player = [t for t in valid_2p_teams if user_id in t]
      if not valid_2p_teams_for_player:
        teams_2p_for_player = self.__generate_2p_teams_for_player(user_id)
        valid_2p_teams_for_player = [t for t in teams_2p_for_player if
                                         all(p in current_players for p in t)]
        valid_2p_teams += valid_2p_teams_for_player
      # 3p teams
      valid_3p_teams_for_player = [t for t in valid_3p_teams if user_id in t]
      if not valid_3p_teams_for_player:
        teams_3p_for_player = self.__generate_3p_teams_for_player(user_id)
        valid_3p_teams_for_player = [t for t in teams_3p_for_player if
                                         all(p in current_players for p in t)]
        valid_3p_teams += valid_3p_teams_for_player

      if len(current_players) == 3:
        teams_for_player = [t for t in valid_3p_teams if user_id in t]
        team = choice(teams_for_player)  # nosec
        valid_3p_teams.remove(team)
        self.__teams_3p.remove(team)
      else:
        teams_for_player = [t for t in valid_2p_teams if user_id in t]
        team = choice(teams_for_player)  # nosec
        valid_2p_teams.remove(team)
        self.__teams_2p.remove(team)
      for p in team:
        current_players.remove(p)

      valid_2p_teams = [t for t in valid_2p_teams if not any(p in t for p in team)]
      valid_3p_teams = [t for t in valid_3p_teams if not any(p in t for p in team)]

      teams.append(list(team))

    self.save()

    return teams

  def __generate_2p_teams_for_player(self, user_id):
    teams = []
    others = [p for p in self.__players if p != user_id]
    for player in others:
      new_team = (user_id, player)
      self.__teams_2p.add(new_team)
      teams.append(new_team)
    return teams

  def __generate_3p_teams_for_player(self, user_id):
    teams = []
    others = [p for p in self.__players if p != user_id]
    all_2p_teams = itertools.combinations(others, 2)
    for t2p in all_2p_teams:
      new_team = (user_id, t2p[0], t2p[1])
      self.__teams_3p.add(new_team)
      teams.append(new_team)
    return teams

  def __set_players(self, players):
    # Generate teams for added players
    new_players = [p for p in players if p not in self.__players]
    for new_player in new_players:
      self.__generate_2p_teams_for_player(new_player)
      self.__generate_3p_teams_for_player(new_player)
      self.__players.append(new_player)

  def __get_teams_2p(self):
    if not self.__teams_2p:
      self.__teams_2p = set(itertools.combinations(self.__players, 2))
    return self.__teams_2p

  def __get_teams_3p(self):
    if not self.__teams_3p:
      self.__teams_3p = set(itertools.combinations(self.__players, 3))
    return self.__teams_3p

  def file_path(self):
    return os.path.expanduser("{}/teams.json".format(DATA_PATH))

  def reset(self):
    self.__teams_2p = set()
    self.__teams_3p = set()
    self.__players = []

  def save(self):
    data = {
      "players": list(self.__players),
      "teams_2p": list(self.__get_teams_2p()),
      "teams_3p": list(self.__get_teams_3p())
    }
    os.makedirs(os.path.dirname(self.file_path()), exist_ok=True)
    with open(self.file_path(), "w+") as fp:
      json.dump(data, fp, indent=2)

  def load(self):
    with open(self.file_path(), "r") as fp:
      data = json.load(fp)
      if "players" in data:
        self.__players = set(data["players"])
      if "teams_2p" in data:
        teams_2p = data["teams_2p"]
        self.__teams_2p = set(map(tuple, teams_2p))
      if "teams_3p" in data:
        teams_3p = data["teams_3p"]
        self.__teams_3p = set(map(tuple, teams_3p))
