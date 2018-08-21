import os
import json

from .constants import DATA_PATH

class Config:
  __instance = None

  def __init__(self):
    if not Config.__instance:
      self.reset()

      try:
        self.load()
      except Exception as ex:
        print("Config file could not load: {}".format(self.file_path()))
        print(ex)

      # Save default config if it doesn't exist.
      if not os.path.exists(self.file_path()):
        print("Saving default config: {}".format(self.file_path()))
        self.save()

      Config.__instance = self

  @staticmethod
  def get():
    if not Config.__instance:
      return Config()
    return Config.__instance

  def privileged_users(self):
    return self.__privileged_users

  def file_path(self):
    return os.path.expanduser("{}/config.json".format(DATA_PATH))

  def reset(self):
    self.__privileged_users = []

  def save(self):
    data = {
      "privileged_users": self.privileged_users(),
    }
    os.makedirs(os.path.dirname(self.file_path()), exist_ok=True)
    with open(self.file_path(), "w+") as fp:
      json.dump(data, fp, indent=2)

  def load(self):
    with open(self.file_path(), "r") as fp:
      data = json.load(fp)
      if "privileged_users" in data:
        self.__privileged_users = data["privileged_users"]
