from .achievement import Achievement
from .behavior import WIN_BEHAVIOR

class FlawlessVictoryAchievement(Achievement):
  def __init__(self):
    super(FlawlessVictoryAchievement, self).__init__("FlawlessVictory")

  def name(self):
    return "Flawless Victory"

  def description(self):
    return "Win a perfect match."

  def accepted_behaviors(self):
    return [WIN_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    if user_id not in self.data:
      self.data[user_id] = False
    if behavior.loser_score() == 0 and not self.data[user_id]:
      self.data[user_id] = True
      return True
    return False

  def achieved(self, user_id):
    return user_id in self.data and self.data[user_id]
