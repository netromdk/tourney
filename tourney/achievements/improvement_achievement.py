from .tiered_achievement import TieredAchievement
from .behavior import SEASON_START_BEHAVIOR
from tourney.stats import Stats
from tourney.util import nth_last_season_filter

class SelfImprovementAchievement(TieredAchievement):
  def __init__(self):
    tiers = (
      (1,  "Harder",   "Improve your end-of-season ranking."),
      (4,  "Better",   "Improve your end-of-season ranking four times."),
      (6,  "Faster",   "Improve your end-of-season ranking six times."),
      (12, "Stronger", "Improve your end-of-season ranking twelve times."),
    )
    super(SelfImprovementAchievement, self).__init__("SelfImprovement", tiers)

  def accepted_behaviors(self):
    return [SEASON_START_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    self.check_init(user_id)
    if not self.data[user_id][0]:
      stats = Stats.get()

      stats.generate(time_filter=nth_last_season_filter(1))
      placement = stats.local_placement(user_id)
      if placement is None:
        return False

      stats.generate(time_filter=nth_last_season_filter(2))
      placement_prev = stats.local_placement(user_id)
      if placement_prev is None:
        return False

      # Check if placement is better (smaller).
      if placement < placement_prev:
        self.data[user_id][0] += 1
        amount = self.data[user_id][0]
        nt = self.next_tier(user_id)
        if amount == nt:
          self.data[user_id][1] += 1
          return True
    return False
