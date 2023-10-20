from datetime import date

from tourney.stats import Stats
from tourney.util import nth_last_season_filter

from .tiered_achievement import TieredAchievement
from .behavior import SEASON_START_BEHAVIOR

class SelfImprovementAchievement(TieredAchievement):
  def __init__(self):
    tiers = (
      (1,  "Harder",   "Improve your end-of-season ranking."),
      (4,  "Better",   "Improve your end-of-season ranking four times."),
      (6,  "Faster",   "Improve your end-of-season ranking six times."),
      (12, "Stronger", "Improve your end-of-season ranking twelve times."),
      (24, "Mightier", "Improve your end-of-season ranking twenty four times."),
    )
    super().__init__("SelfImprovement", tiers)

  def accepted_behaviors(self):
    return [SEASON_START_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    self.check_init(user_id)

    today = date.today()
    if today.month == 1:
      last_season = [today.year - 1, 12]
    else:
      last_season = [today.year, today.month - 1]

    if isinstance(self.data[user_id][0], int):
      self.data[user_id][0] = [0]
    if last_season in self.data[user_id][0]:
      # Already scored
      return False

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
      self.data[user_id][0].append(last_season)
      amount = len(self.data[user_id][0])
      nt = self.next_tier(user_id)
      if amount >= nt:
        self.data[user_id][1] += 1
        return True

    return False

  def progress(self, user_id):
    self.check_init(user_id)
    return len(self.data[user_id][0])

  def check_init(self, user_id):
    if user_id not in self.data:
      self.data[user_id] = [
         [],     # List of achieved seasons
         -1,     # Tier
      ]
