from .tiered_achievement import TieredAchievement
from .behavior import SEASON_START_BEHAVIOR
from datetime import date
from tourney.stats import Stats
from tourney.util import nth_last_season_filter

class SeasonTopFiveAchievement(TieredAchievement):
  def __init__(self):
    tiers = (
      (1,  "Fairest of the Season",      "End a season in the top five by wins "
         "while participating in a significant number of matches."),
      (4,  "Vivaldi",    "End four seasons in the top five by wins "
         "while participating in a significant number of matches."),
      (12, "A Very Good Year", "End twelve seasons in the top five by wins "
         "while participating in a significant number of matches."),
    )
    super(SeasonTopFiveAchievement, self).__init__("SeasonTopFive", tiers)

  def accepted_behaviors(self):
    return [SEASON_START_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    stats = Stats.get()

    stats.generate(time_filter=nth_last_season_filter(1))

    top_five = stats.get_top_winners()[:5]

    # The description is slightly misleading. You need to appear in 1/4 as
    # many matches as the person with the most matches, not the total amount.
    # This way if there's a weird season where a new set of people play each
    # week of the month they don't all get cheated of the achievement.
    most_matches = 0
    personals = stats.get_personals()
    for uid in personals:
      self.check_init(uid)
      personal = uid
      if "total_matches" in personal:
        most_matches = max(most_matches, personals[uid]["total_matches"])

    if most_matches == 0:
      return False

    today = date.today()
    if today.month == 1:
      last_season = (today.year - 1, 12)
    else:
      last_season = (today.year, today.month - 1)

    self.check_init(user_id)

    if last_season not in self.data[user_id][0] \
          and personals[user_id]["total_matches"] >= most_matches / 4\
          and user_id in top_five:
      self.data[user_id][0].append(last_season)
      amount = len(self.data[user_id][0])
      nt = self.next_tier(user_id)
      if amount == nt:
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
