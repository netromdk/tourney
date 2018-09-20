from .behavior import Behavior, REPORT_SCORE_BEHAVIOR

class ReportScoreBehavior(Behavior):
  def __init__(self, user_id):
    super(ReportScoreBehavior, self).__init__(REPORT_SCORE_BEHAVIOR, user_id)
