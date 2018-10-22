from .tiered_achievement import TieredAchievement
from .behavior import REPORT_SCORE_BEHAVIOR

class ReporterAchievement(TieredAchievement):
  def __init__(self):
    tiers = (
      (1,    "Reporter",           "Reported a score."),
      (10,   "Journalist",         "Reported 10 scores."),
      (25,   "Correspondent",      "Reported 25 scores."),
      (30,   "Jes Dorph Petersen", "Reported 30 scores."),
      (40,   "Steen Bostrup",      "Reported 40 scores."),
      (50,   "Anchorman",          "Reported 50 scores."),
      (75,   "Mette Fugl",         "Reported 75 scores."),
      (100,  "Ulla Terkelsen",     "Reported 100 scores."),
      (500,  "Larry King",         "Reported 500 scores."),
      (1000, "Walter Cronkite",    "Reported 1000 scores."),
    )
    super(ReporterAchievement, self).__init__("Reporter", tiers)

  def accepted_behaviors(self):
    return [REPORT_SCORE_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    self.check_init(user_id)
    self.data[user_id][0] += 1
    amount = self.data[user_id][0]
    if amount == self.next_tier(user_id):
      self.data[user_id][1] += 1
      return True
    return False
