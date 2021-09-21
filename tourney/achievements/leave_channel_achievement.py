from .tiered_achievement import TieredAchievement
from .behavior import LEAVE_CHANNEL_BEHAVIOR

class LeaveChannelAchievement(TieredAchievement):
  def __init__(self):
    tiers = (
      (1,  "Hasta la Vista",          "Leave the channel."),
      (5,  "Be Seeing You",           "Leave the channel 5 times."),
      (10, "I Wish I Could Quit You", "Leave the channel 10 times."),
    )
    super(LeaveChannelAchievement, self).__init__("LeaveChannel", tiers)

  def accepted_behaviors(self):
    return [LEAVE_CHANNEL_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    self.check_init(user_id)
    self.data[user_id][0] += 1
    amount = self.data[user_id][0]
    if amount == self.next_tier(user_id):
      self.data[user_id][1] += 1
      return True
    return False
