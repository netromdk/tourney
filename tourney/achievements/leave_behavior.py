from .behavior import Behavior, LEAVE_BEHAVIOR

class LeaveBehavior(Behavior):
  def __init__(self, user_id):
    super().__init__(LEAVE_BEHAVIOR, user_id)
