from .behavior import Behavior, WIN_BEHAVIOR

class WinBehavior(Behavior):
  def __init__(self, user_id, rounds):
    super(WinBehavior, self).__init__(WIN_BEHAVIOR, user_id)
    self.__rounds = rounds

  def rounds(self):
    return self.__rounds
