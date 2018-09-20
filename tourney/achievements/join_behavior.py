from .behavior import Behavior, JOIN_BEHAVIOR

class JoinBehavior(Behavior):
  def __init__(self, user_id):
    super(JoinBehavior, self).__init__(JOIN_BEHAVIOR, user_id)
