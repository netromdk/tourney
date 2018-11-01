from .tiered_achievement import TieredAchievement
from .behavior import WIN_BEHAVIOR

class WinnerAchievement(TieredAchievement):
  def __init__(self):
    tiers = (
      (1,   "Bronze Winner", "Win 1 round."),
      (10,  "Silver Winner", "Win 10 rounds."),
      (100, "Gold Winner",   "Win 100 rounds."),
    )
    super(WinnerAchievement, self).__init__("Winner", tiers)

  def accepted_behaviors(self):
    return [WIN_BEHAVIOR]

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
