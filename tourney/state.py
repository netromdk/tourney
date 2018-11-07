import os
import json

from .constants import DATA_PATH, DEMO

class State:
  __instance = None

  def __init__(self):
    if not State.__instance:
      self.reset()
      try:
        self.load()
      except Exception as ex:
        print("State file could not load: {}".format(self.file_path()))
        print(ex)

      State.__instance = self

  @staticmethod
  def get():
    if not State.__instance:
      return State()
    return State.__instance

  def set_bot_id(self, bot_id):
    self.__bot_id = bot_id

  def bot_id(self):
    if DEMO:
      return "DEMO_BOT_ID"
    return self.__bot_id

  def set_channel_id(self, channel_id):
    self.__channel_id = channel_id

  def channel_id(self):
    if DEMO:
      return "#DEMOCHANNEL"
    return self.__channel_id

  def set_participants(self, participants):
    self.__participants = participants

  def add_participant(self, participant):
    self.__participants.append(participant)

  def remove_participant(self, participant):
    self.__participants.remove(participant)

  def participants(self):
    return self.__participants

  def set_morning_announce(self, ts):
    self.__morning_announce = ts

  def morning_announce(self):
    return self.__morning_announce

  def set_reminder_announce(self, ts):
    self.__reminder_announce = ts

  def reminder_announce(self):
    return self.__reminder_announce

  def set_midday_announce(self, midday_announce):
    self.__midday_announce = midday_announce

  def midday_announce(self):
    return self.__midday_announce

  def set_schedule(self, schedule):
    self.__schedule = schedule

  def schedule(self):
    return self.__schedule

  def set_teams(self, teams):
    self.__teams = teams

  def teams(self):
    return self.__teams

  def set_team_names(self, team_names):
    self.__team_names = team_names

  def team_names(self):
    return self.__team_names

  def set_unrecorded_matches(self, unrecorded_matches):
    self.__unrecorded_matches = unrecorded_matches

  def unrecorded_matches(self):
    return self.__unrecorded_matches

  def set_dont_remind_users(self, dont_remind_users):
    self.__dont_remind_users = dont_remind_users

  def add_dont_remind_user(self, user_id):
    self.__dont_remind_users.append(user_id)

  def dont_remind_users(self):
    return self.__dont_remind_users

  def file_path(self):
    return os.path.expanduser("{}/state.json".format(DATA_PATH))

  def reset(self):
    self.__bot_id = None
    self.__channel_id = None
    self.__participants = []
    self.__morning_announce = None
    self.__reminder_announce = None
    self.__midday_announce = False
    self.__schedule = []
    self.__teams = []
    self.__team_names = []
    self.__unrecorded_matches = []
    self.__dont_remind_users = []

  def save(self):
    data = {
      "bot_id": self.__bot_id,
      "channel_id": self.__channel_id,
      "participants": self.__participants,
      "morning_announce": self.__morning_announce,
      "reminder_announce": self.__reminder_announce,
      "midday_announce": self.__midday_announce,
      "schedule": self.__schedule,
      "teams": self.__teams,
      "team_names": self.__team_names,
      "unrecorded_matches": self.__unrecorded_matches,
      "dont_remind_users": self.__dont_remind_users
    }
    os.makedirs(os.path.dirname(self.file_path()), exist_ok=True)
    with open(self.file_path(), "w+") as fp:
      json.dump(data, fp, indent=2)

  def load(self):
    with open(self.file_path(), "r") as fp:
      data = json.load(fp)
      if "bot_id" in data:
        self.set_bot_id(data["bot_id"])
      if "channel_id" in data:
        self.set_channel_id(data["channel_id"])
      if "participants" in data:
        self.set_participants(data["participants"])
      if "morning_announce" in data:
        self.set_morning_announce(data["morning_announce"])
      if "reminder_announce" in data:
        self.set_reminder_announce(data["reminder_announce"])
      if "midday_announce" in data:
        self.set_midday_announce(data["midday_announce"])
      if "schedule" in data:
        self.set_schedule(data["schedule"])
      if "teams" in data:
        self.set_teams(data["teams"])
      if "team_names" in data:
        self.set_team_names(data["team_names"])
      if "unrecorded_matches" in data:
        self.set_unrecorded_matches(data["unrecorded_matches"])
      if "dont_remind_users" in data:
        self.set_dont_remind_users(data["dont_remind_users"])
