from .achievement import Achievement
from .behavior import WIN_BEHAVIOR

TIERS = (
  (1,   "Three Amigos", "Win a match in a three-player team."),
  (3,   "Three Musketeers", "Win three matches in three-player teams."),
)

class ThreePlayerWinAchievement(Achievement):
  def __init__(self):
    super(ThreePlayerWinAchievement, self).__init__("ThreePlayerWin")

  def name(self):
    return TIERS[0][1]

  def description(self):
    return TIERS[0][2]

  def accepted_behaviors(self):
    return [WIN_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    user_team = behavior.winner_team()
    self.__check_init(user_id)
    if len(user_team) == 3:
      self.data[user_id][0] += 1
      amount = self.data[user_id][0]
      nt = self.next_tier(user_id)
      if amount == nt or amount == nt+1:
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
         0, # Won rounds amount
        -1, # Tier
      ]
