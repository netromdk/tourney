from .achievement import Achievement
from .behavior import WIN_BEHAVIOR

class WinGoldenGoalAchievement(Achievement):
  def __init__(self):
    super(WinGoldenGoalAchievement, self).__init__("WinGoldenGoal")

  def name(self):
    return "No Sweat"

  def description(self):
    return "Win a match at Golden Goal."

  def accepted_behaviors(self):
    return [WIN_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    if user_id not in self.data:
      self.data[user_id] = False
    if (behavior.winner_score() - 1 == behavior.loser_score()) and not self.data[user_id]:
      self.data[user_id] = True
      return True
    return False

  def achieved(self, user_id):
    return user_id in self.data and self.data[user_id]
