from .achievement import Achievement
from .behavior import INVOKE_BEHAVIOR

TIERS = (
  (10,  "Commander",                    "Invoke 10 commands."),
  (20,  "Commander Lieutenant",         "Invoke 20 commands."),
  (30,  "Commander Captain",            "Invoke 30 commands."),
  (40,  "Commander Major",              "Invoke 40 commands."),
  (50,  "Commander Major General",      "Invoke 50 commands."),
  (75,  "Commander Lieutenant General", "Invoke 75 commands."),
  (150, "Commander General",            "Invoke 150 commands."),
  (300, "Commander Field Marshal",      "Invoke 300 commands."),
)

class CommanderAchievement(Achievement):
  def __init__(self):
    super(CommanderAchievement, self).__init__("Commander")

  def name(self):
    return TIERS[0][1]

  def description(self):
    return TIERS[0][2]

  def accepted_behaviors(self):
    return [INVOKE_BEHAVIOR]

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
         0, # Command amount
        -1, # Tier
      ]
