import os
import json
from random import choice

from .constants import DATA_PATH, TEAM_NAMES

class Teamnames:
  __instance = None

  def __init__(self):
    if not Teamnames.__instance:
      self.reset()
      try:
        self.load()
      except Exception as ex:
        print("Team name file could not load: {}".format(self.file_path()))
        print(ex)

      Teamnames.__instance = self

  @staticmethod
  def get():
    if not Teamnames.__instance:
      return Teamnames()
    return Teamnames.__instance

  def add(self, team, teamname):
    """Add a teamname for a given team."""
    self.__teamnames = [x for x in self.__teamnames if x[0] != team]
    self.__teamnames.append([team, teamname])

  def teamname(team):
    if team in self.__teamnames:
      return self.__teamnames[team]
    else:
      return choice(TEAM_NAMES)  # nosec

  def file_path(self):
    return os.path.expanduser("{}/teamnames.json".format(DATA_PATH))

  def reset(self):
    self.__teamnames = []

  def save(self):
    data = {
      "teamnames": self.__teamnames,
    }
    os.makedirs(os.path.dirname(self.file_path()), exist_ok=True)
    with open(self.file_path(), "w+") as fp:
      json.dump(data, fp)

  def load(self):
    with open(self.file_path(), "r") as fp:
      data = json.load(fp)
      if "teamnames" in data:
        self.__teamnames = data["teamnames"]
