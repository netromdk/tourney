from .achievement import Achievement
from .behavior import REPORT_SCORE_BEHAVIOR

class ReportOtherAchievement(Achievement):
  def __init__(self):
    super(ReportOtherAchievement, self).__init__("ReportOther")

  def name(self):
    return "Snitch"

  def description(self):
    return "Report a match you weren't in"

  def accepted_behaviors(self):
    return [REPORT_SCORE_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    winner_team = behavior.winner_team()
    loser_team = behavior.loser_team()
    if user_id not in winner_team and user_id not in loser_team:
      self.data[user_id][1] = True
      return True
    return False

  def achieved(self, user_id):
    return user_id in self.data and self.data[user_id]
