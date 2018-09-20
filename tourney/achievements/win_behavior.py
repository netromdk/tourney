from .behavior import Behavior, WIN_BEHAVIOR

class WinBehavior(Behavior):
  def __init__(self, user_id):
    super(WinBehavior, self).__init__(WIN_BEHAVIOR, user_id)
