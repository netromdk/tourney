import os
import json
from datetime import datetime, timedelta

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
      print("Scores loaded from: {}".format(self.file_path()))
