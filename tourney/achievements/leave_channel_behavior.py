from .behavior import Behavior, LEAVE_CHANNEL_BEHAVIOR

class LeaveChannelBehavior(Behavior):
  def __init__(self, user_id):
    super().__init__(LEAVE_CHANNEL_BEHAVIOR, user_id)
