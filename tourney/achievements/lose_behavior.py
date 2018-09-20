from .behavior import Behavior, LOSE_BEHAVIOR

class LoseBehavior(Behavior):
  def __init__(self, user_id, rounds):
    super(LoseBehavior, self).__init__(LOSE_BEHAVIOR, user_id)
    self.__rounds = rounds

  def rounds(self):
    return self.__rounds
