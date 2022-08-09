from .tiered_achievement import TieredAchievement
from .behavior import JOIN_BEHAVIOR

class ParticipationAchievement(TieredAchievement):
  def __init__(self):
    tiers = (
      (5,   "Bronze Participation Trophy", "Join 5 games."),
      (50,  "Silver Participation Trophy", "Join 50 games."),
      (100, "Gold Participation Trophy",   "Join 100 games."),
    )
    super().__init__("Participation", tiers)

  def accepted_behaviors(self):
    return [JOIN_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    self.check_init(user_id)
    self.data[user_id][0] += 1
    amount = self.data[user_id][0]
    if amount == self.next_tier(user_id):
      self.data[user_id][1] += 1
      return True
    return False
