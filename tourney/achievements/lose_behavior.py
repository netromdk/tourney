from .behavior import Behavior, LOSE_BEHAVIOR

class LoseBehavior(Behavior):
  def __init__(self, user_id, rounds, winner_score, loser_score):
    super(LoseBehavior, self).__init__(LOSE_BEHAVIOR, user_id)
    self.__rounds = rounds
    self.__winner_score = winner_score
    self.__loser_score = loser_score

  def rounds(self):
    return self.__rounds

  def winner_score(self):
    return self.__winner_score

  def loser_score(self):
    return self.__loser_score
