from .achievement import Achievement
from .behavior import LOSE_BEHAVIOR

class LoseGoldenGoalAchievement(Achievement):
  def __init__(self):
    super(LoseGoldenGoalAchievement, self).__init__("LoseGoldenGoal")

  def name(self):
    return "No Cigar"

  def description(self):
    return "Lose a match at Golden Goal."

  def accepted_behaviors(self):
    return [LOSE_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    if not user_id in self.data:
      self.data[user_id] = False
    if (behavior.winner_score()-1 == behavior.loser_score()) and not self.data[user_id]:
      self.data[user_id] = True
      return True
    return False

  def achieved(self, user_id):
    return user_id in self.data and self.data[user_id]

  def progress(self, user_id):
    return 0

  def next_tier(self, user_id):
    return None

  def tiered_name(self, user_id):
    return self.name()

  def tiered_description(self, user_id):
    return self.description()
