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

  def pick_pairs(self, n):
    return [2 for x in range(0, n - 1, 2)]

  def place_single(self, teams):
    try:
      idx2 = teams.index(2)
      duo = teams.pop(idx2)
      duo = duo + 1
      teams.append(duo)
    except ValueError:
      pass

  def split_to_singles(self, teams):
    team = teams.pop(0)
    for i in range(team):
      teams.append(1)

  def even_teams(self, teams):
    # Get a 2-person team:
    team = None
    try:
      idx = teams.index(2)
      team = teams.pop(idx)
    except ValueError:
      pass

    # Find two other 2-player teams to split onto:
    if team:
      open_teams = []
      try:
        for i in range(team):
          idx = teams.index(2)
          open_teams.append(teams.pop(idx))

        # Put each player of the team on 2-person teams
        for open_team in open_teams:
          open_team = open_team + 1
          teams.append(open_team)
      except ValueError:
        # No 2-person teams found, put all teams back where we found them
        for open_team in open_teams:
          teams.append(open_team)
        open_teams.clear()
        teams.append(team)

  def split_teams(self, n):
    teams = []

    # First make as many 2-person teams as possible
    teams = self.pick_pairs(n)

    # If there's a player left over, stick him on a 2-person team
    if n % 2 == 1:
      self.place_single(teams)

    if len(teams) == 1:
      # If that just gives the one team, split it into singles
      self.split_to_singles(teams)

    # If this gives an odd number of teams, try splitting a two man team across two 2-person teams
    if len(teams) % 2 != 0:
      self.even_teams(teams)

    return teams

  def get_teams_for_players(self, current_players):
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

        for user_id in team:
          # Remove other teams with players
          valid_teams[2] = [t for t in valid_teams[2] if user_id not in t]
          valid_teams[3] = [t for t in valid_teams[3] if user_id not in t]
          current_players.remove(user_id)

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
      self.__players.add(new_player)

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
