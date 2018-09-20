from .behavior import Behavior, WIN_BEHAVIOR

class WinBehavior(Behavior):
  def __init__(self, user_id, rounds, winner_score, loser_score):
    super(WinBehavior, self).__init__(WIN_BEHAVIOR, user_id)
    self.__rounds = rounds
    self.__winner_score
    self.__loser_score

  def rounds(self):
    return self.__rounds

  def winner_score(self):
    return self.__winner_score

  def loser_score(self):
    return self.__loser_score
