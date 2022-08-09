from .behavior import Behavior, REPORT_SCORE_BEHAVIOR

class ReportScoreBehavior(Behavior):
  def __init__(self, user_id, winner_team, loser_team):
    super().__init__(REPORT_SCORE_BEHAVIOR, user_id)
    self.__winner_team = winner_team
    self.__loser_team = loser_team

  def winner_team(self):
    return self.__winner_team

  def loser_team(self):
    return self.__loser_team
