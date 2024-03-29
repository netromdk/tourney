from .tiered_achievement import TieredAchievement
from .behavior import JOIN_BEHAVIOR

class ParticipationAchievement(TieredAchievement):
  def __init__(self):
    tiers = (
      (5,    "Bronze Participation Trophy",     "Join 5 games."),
      (50,   "Silver Participation Trophy",     "Join 50 games."),
      (100,  "Gold Participation Trophy",       "Join 100 games."),
      (500,  "Platinum Participation Trophy",   "Join 500 games."),
      (1000, "Adamantium Participation Trophy", "Join 1000 games."),
      (2000, "Unobtanium Participation Trophy", "Join 2000 games."),
    )
    super().__init__("Participation", tiers)

  def accepted_behaviors(self):
    return [JOIN_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    self.check_init(user_id)
    self.data[user_id][0] += 1
    amount = self.data[user_id][0]
    nt = self.next_tier(user_id)
    if nt is not None and amount >= nt:
      self.data[user_id][1] += 1
      return True
    return False
