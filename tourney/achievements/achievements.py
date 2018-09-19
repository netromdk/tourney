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
      if achiev.accepts(behavior.kind()) and achiev.update(behavior):
        self.__broadcast_achievement(behavior.user_id(), achiev)
    self.save()

  def __broadcast_achievement(self, user_id, achiev):
    # TODO: Post to slack!
    print("{} achieved: {}".format(user_id, achiev.current_progress(user_id)))

  def user_response(self, user_id):
    """Returns formatted response with user progress of all achievements."""
    res = []
    for achiev in self.__achievements:
      if achiev.achieved(user_id) or achiev.progress(user_id) > 0:
        res.append(achiev.current_progress(user_id))
    return "Achievements progress:\n\t" + "\n\t".join(res)

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
      achiev_data[achiev.kind()] = achiev.data
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
