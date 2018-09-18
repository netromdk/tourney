import os
import json

from tourney.constants import DATA_PATH

class Achievements:
  __instance = None

  def __init__(self):
    if not Achievements.__instance:
      self.reset()
      try:
        self.load()
      except Exception as ex:
        print("Achievements file could not load: {}".format(self.file_path()))
        print(ex)

      Achievements.__instance = self

  @staticmethod
  def get():
    if not Achievements.__instance:
      return Achievements()
    return Achievements.__instance

  def file_path(self):
    return os.path.expanduser("{}/achievements.json".format(DATA_PATH))

  def reset(self):
    # Achievement instances.
    self.__achievements = []
    # TODO: Lead each kind of achievement as instances.

  def save(self):
    # TODO: Serialize each achievement instance's data and save as kind -> data.
    data = {
      "data": {}
    }
    os.makedirs(os.path.dirname(self.file_path()), exist_ok=True)
    with open(self.file_path(), "w+") as fp:
      json.dump(data, fp, indent=2)

  def load(self):
    with open(self.file_path(), "r") as fp:
      data = json.load(fp)
      if "data" in data:
        # TODO: Deserialize each kind -> data for associated achievement instance.
        pass
