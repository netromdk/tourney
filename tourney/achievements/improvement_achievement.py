from .tiered_achievement import TieredAchievement
from .behavior import SEASON_START_BEHAVIOR
from datetime import date, datetime
from tourney.stats import Stats
from tourney.util import last_season_filter

class SelfImprovementAchievement(TieredAchievement):
  def __init__(self):
    tiers = (
      (1,  "Harder",   "Improve your end-of-season ranking."),
      (4,  "Better",   "Improve your end-of-season ranking four times."),
      (6,  "Faster",   "Improve your end-of-season ranking six times."),
      (12, "Stronger", "Improve your end-of-season ranking twelve times."),
    )
    super(SelfImprovementAchievement, self).__init__("SelvImprovement", tiers)

  def accepted_behaviors(self):
    return [SEASON_START_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    self.check_init(user_id)
    if not self.data[user_id][0]:
      stats = Stats.get()

      def season_before_last_filter(match_stamp):
        today = date.today()
        match = datetime.fromtimestamp(match_stamp)
        if today.month == 1:
          return match.month == 11 and match.year == today.year - 1
        elif today.month == 2:
          return match.month == 12 and match.year == today.year - 1
        else:
          return match.month == today.month - 2 and match.year == today.year

      stats.generate(time_filter=season_before_last_filter)
      personals = stats.get_personals()
      if user_id not in personals:
        return False

      stats.generate(time_filter=last_season_filter)
      personals_prev = stats.get_personals()
      if user_id not in personals_prev:
        return False

      wins_prev = personals_prev[user_id]["total_wins"]
      wins = personals[user_id]["total_wins"]
      if wins_prev > wins:
        self.data[user_id][0] += 1
        amount = self.data[user_id][0]
        nt = self.next_tier(user_id)
        if amount == nt:
          self.data[user_id][1] += 1
          return True
    return False
