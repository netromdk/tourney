from .achievement import Achievement
from .behavior import LEAVE_CHANNEL_BEHAVIOR

TIERS = (
  (1,  "Sore",                    "Leave the channel."),
  (5,  "Detoxing",                "Leave the channel 5 times."),
  (10, "I Wish I Could Quit You", "Leave the channel 10 times."),
)

class LeaveChannelAchievement(Achievement):
  def __init__(self):
    super(LeaveChannelAchievement, self).__init__("LeaveChannel")

  def name(self):
    return TIERS[0][1]

  def description(self):
    return TIERS[0][2]

  def accepted_behaviors(self):
    return [LEAVE_CHANNEL_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    self.__check_init(user_id)
    self.data[user_id][0] += 1
    amount = self.data[user_id][0]
    if amount == self.next_tier(user_id):
      self.data[user_id][1] += 1
      return True
    return False

  def achieved(self, user_id):
    self.__check_init(user_id)
    return self.data[user_id][1] >= 0

  def progress(self, user_id):
    self.__check_init(user_id)
    return self.data[user_id][0]

  def next_tier(self, user_id):
    self.__check_init(user_id)
    tier = self.data[user_id][1]
    nt = tier+1
    if nt >= len(TIERS):
      return None
    return TIERS[nt][0]

  def tiered_name(self, user_id):
    self.__check_init(user_id)
    tier = self.data[user_id][1]
    if tier == -1:
      return self.name()
    return TIERS[tier][1]

  def tiered_description(self, user_id):
    self.__check_init(user_id)
    tier = self.data[user_id][1]
    if tier == -1:
      return self.description()
    return TIERS[tier][2]

  def __check_init(self, user_id):
    if user_id not in self.data:
      self.data[user_id] = [
         0, # Amount of times leaving channel.
        -1, # Tier
      ]
