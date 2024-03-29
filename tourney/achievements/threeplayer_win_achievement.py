from .tiered_achievement import TieredAchievement
from .behavior import WIN_BEHAVIOR

class ThreePlayerWinAchievement(TieredAchievement):
  def __init__(self):
    tiers = (
      (1,   "Three Amigos", "Win a match in a three-player team."),
      (3,   "Three Musketeers", "Win three matches in three-player teams."),
      (33,  "Three Kings", "Win thirty three matches in three-player teams."),
      (333, "Holy Trinity", "Win three hundred and thirty three matches in three-player teams."),
    )
    super().__init__("ThreePlayerWin", tiers)

  def accepted_behaviors(self):
    return [WIN_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    user_team = behavior.winner_team()
    self.check_init(user_id)
    if len(user_team) == 3:
      self.data[user_id][0] += 1
      amount = self.data[user_id][0]
      nt = self.next_tier(user_id)
      if amount == nt:
        self.data[user_id][1] += 1
        return True
    return False
