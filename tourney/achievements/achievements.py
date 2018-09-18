import os
import json

from .rtfm_achievement import RtfmAchievement

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

  def interact(self, behavior):
    """Interact given specified behavior and update with each achievement accepting it."""
    for achiev in self.__achievements:
      if achiev.accepts(behavior.kind()):
        achiev.update(behavior)
        # TODO: Check if achievement was obtained via the behavior.
    self.save()

  def file_path(self):
    return os.path.expanduser("{}/achievements.json".format(DATA_PATH))

  def reset(self):
    # Achievement instances.
    self.__achievements = [
      RtfmAchievement()
    ]

  def save(self):
    # Serialize each achievement instance's data and save as kind -> data.
    achiev_data = {}
    for achiev in self.__achievements:
      achiev_data[achiev.kind()] = achiev.data()
    data = {
      "data": achiev_data
    }
    os.makedirs(os.path.dirname(self.file_path()), exist_ok=True)
    with open(self.file_path(), "w+") as fp:
      json.dump(data, fp, indent=2)

  def load(self):
    with open(self.file_path(), "r") as fp:
      data = json.load(fp)
      if "data" in data:
        # Deserialize each kind -> data for associated achievement instance.
        achiev_data = data["data"]
        for achiev in self.__achievements:
          if achiev.kind() in achiev_data:
            achiev.set_data(achiev_data[achiev.kind()])
