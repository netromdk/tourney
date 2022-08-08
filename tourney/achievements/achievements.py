import os
import json

from .rtfm_achievement import RtfmAchievement
from .commander_achievement import CommanderAchievement
from .participation_achievement import ParticipationAchievement
from .winner_achievement import WinnerAchievement
from .loser_achievement import LoserAchievement
from .win_golden_goal_achievement import WinGoldenGoalAchievement
from .lose_golden_goal_achievement import LoseGoldenGoalAchievement
from .obsessed_achievement import ObsessedAchievement
from .self_obsessed_achievement import SelfObsessedAchievement
from .flawless_victory_achievement import FlawlessVictoryAchievement
from .flawless_defeat_achievement import FlawlessDefeatAchievement
from .reporter_achievement import ReporterAchievement
from .leave_channel_achievement import LeaveChannelAchievement
from .first_joiner_achievement import FirstJoinerAchievement
from .snitch_achievement import ReportOtherAchievement
from .spelling_achievement import SpellingAchievement
from .threeplayer_win_achievement import ThreePlayerWinAchievement
from .threetwo_win_achievement import ThreeVTwoWinAchievement
from .season_top_five_achievement import SeasonTopFiveAchievement
from .improvement_achievement import SelfImprovementAchievement

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
        self.__save_for_broadcast(behavior.user_id(), achiev)
    self.save()

  def __save_for_broadcast(self, user_id, achiev):
    """Saves obtained achievement response for next scheduled action tick."""
    self.__broadcasts.append((user_id, achiev.current_progress(user_id)))

  def scheduled_broadcasts(self):
    res = self.__broadcasts
    self.__broadcasts = []
    return res

  def user_response(self, user_id):
    """Returns formatted response with user progress of all achievements."""
    res = []
    for achiev in self.__achievements:
      if achiev.achieved(user_id):
        res.append(achiev.current_progress(user_id))
    if len(res) == 0:
      return "No achievements yet!"
    return "Achievements progress:\n\t" + "\n\t".join(res)

  def file_path(self):
    return os.path.expanduser("{}/achievements.json".format(DATA_PATH))

  def reset(self):
    self.__achievements = [
      RtfmAchievement(),
      CommanderAchievement(),
      ParticipationAchievement(),
      WinnerAchievement(),
      LoserAchievement(),
      WinGoldenGoalAchievement(),
      LoseGoldenGoalAchievement(),
      ObsessedAchievement(),
      SelfObsessedAchievement(),
      FlawlessVictoryAchievement(),
      FlawlessDefeatAchievement(),
      ReporterAchievement(),
      LeaveChannelAchievement(),
      FirstJoinerAchievement(),
      ReportOtherAchievement(),
      SpellingAchievement(),
      ThreePlayerWinAchievement(),
      ThreeVTwoWinAchievement(),
      SeasonTopFiveAchievement(),
      SelfImprovementAchievement()
    ]

    # Saved responses of obtained achievements for broadcasting.
    self.__broadcasts = []  # [(user_id, text), ..]

  def save(self):
    # Serialize each achievement instance's data and save as kind -> data.
    achiev_data = {}
    for achiev in self.__achievements:
      achiev_data[achiev.kind()] = achiev.data
    data = {
      "data": achiev_data
    }
    os.makedirs(os.path.dirname(self.file_path()), exist_ok=True)
    with open(self.file_path(), "w+", encoding="utf-8") as fp:
      json.dump(data, fp, indent=2)

  def load(self):
    with open(self.file_path(), "r", encoding="utf-8") as fp:
      data = json.load(fp)
      if "data" in data:
        # Deserialize each kind -> data for associated achievement instance.
        achiev_data = data["data"]
        for achiev in self.__achievements:
          if achiev.kind() in achiev_data:
            achiev.set_data(achiev_data[achiev.kind()])
