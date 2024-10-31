from .tiered_achievement import TieredAchievement
from .behavior import NAME_TEAM_BEHAVIOR

class TeamNamerAchievement(TieredAchievement):
  def __init__(self):
    tiers = (
      (1,    "Team Namer",        "Named one of your teams."),
      (5,    "Inventive",         "Named a team 5 times."),
      (10,   "Branding Expert",   "Named a team 10 times."),
    )
    super(TeamNamerAchievement, self).__init__("Team Namer", tiers)

  def accepted_behaviors(self):
    return [NAME_TEAM_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    self.check_init(user_id)
    self.data[user_id][0] += 1
    amount = self.data[user_id][0]
    if amount == self.next_tier(user_id):
      self.data[user_id][1] += 1
      return True
    return False
