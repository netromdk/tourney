from .tiered_achievement import TieredAchievement
from .behavior import LOSE_BEHAVIOR

class LoserAchievement(TieredAchievement):
  def __init__(self):
    tiers = (
      (1,   "Bad Luck",              "Lose 1 round."),
      (10,  "Extremely Bad Luck",    "Lose 10 rounds."),
      (100, "Unbelievably Bad Luck", "Lose 100 rounds."),
    )
    super(LoserAchievement, self).__init__("Loser", tiers)

  def accepted_behaviors(self):
    return [LOSE_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    self.check_init(user_id)
    self.data[user_id][0] += behavior.rounds()
    amount = self.data[user_id][0]
    nt = self.next_tier(user_id)
    if amount == nt or amount == nt + 1:
      self.data[user_id][1] += 1
      return True
    return False
