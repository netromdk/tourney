from .tiered_achievement import TieredAchievement
from .behavior import INVOKE_BEHAVIOR

class CommanderAchievement(TieredAchievement):
  def __init__(self):
    tiers = (
      (10,  "Commander",                    "Invoke 10 commands."),
      (20,  "Commander Lieutenant",         "Invoke 20 commands."),
      (30,  "Commander Captain",            "Invoke 30 commands."),
      (40,  "Commander Major",              "Invoke 40 commands."),
      (50,  "Commander Major General",      "Invoke 50 commands."),
      (75,  "Commander Lieutenant General", "Invoke 75 commands."),
      (150, "Commander General",            "Invoke 150 commands."),
      (300, "Commander Field Marshal",      "Invoke 300 commands."),
    )
    super(CommanderAchievement, self).__init__("Commander", tiers)

  def accepted_behaviors(self):
    return [INVOKE_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    self.check_init(user_id)
    self.data[user_id][0] += 1
    amount = self.data[user_id][0]
    if amount == self.next_tier(user_id):
      self.data[user_id][1] += 1
      return True
    return False
