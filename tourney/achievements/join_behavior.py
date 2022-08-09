from .behavior import Behavior, JOIN_BEHAVIOR

class JoinBehavior(Behavior):
  def __init__(self, user_id):
    super().__init__(JOIN_BEHAVIOR, user_id)
