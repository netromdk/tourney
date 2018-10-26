from .tiered_achievement import TieredAchievement
from .behavior import WIN_BEHAVIOR

class ThreeVTwoWinAchievement(TieredAchievement):
  def __init__(self):
    tiers = (
      (1,   "Strength in Numbers", "In a three-player team, beat a two player team."),
      (10,  "E Pluribus", "In a three-player team, beat a two player team ten times."),
      (50,  "My Name is Legion", "In a three-player team, beat a two player team fifty times."),
    )
    super(ThreeVTwoWinAchievement, self).__init__("ThreeVTwoWin", tiers)

  def accepted_behaviors(self):
    return [WIN_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    user_team = behavior.winner_team()
    loser_team = behavior.loser_team()
    self.check_init(user_id)
    if len(user_team) == 3 and len(loser_team) == 2:
      self.data[user_id][0] += 1
      amount = self.data[user_id][0]
      nt = self.next_tier(user_id)
      if amount == nt:
        self.data[user_id][1] += 1
        return True
    return False

