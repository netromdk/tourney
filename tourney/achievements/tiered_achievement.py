from .achievement import Achievement

class TieredAchievement(Achievement):
  """Base class for tiered achievements."""

  def __init__(self, kind, tiers):
    """Each tier consists of the goal to achieve it, its title, and its description."""
    super().__init__(kind)
    self.__tiers = tiers

  def name(self):
    return self.__tiers[0][1]

  def description(self):
    return self.__tiers[0][2]

  # Convert from previously untiered achievement
  def convert_from_untiered(self, user_id):
    if user_id in self.data and isinstance(self.data[user_id], bool):
      # Previous, untiered achievement scored
      self.data[user_id] = [
        1,  # Overall progress set to 1
        0,  # First tier achieved
      ]

  def achieved(self, user_id):
    self.check_init(user_id)
    return self.data[user_id][1] >= 0

  def progress(self, user_id):
    self.check_init(user_id)
    return self.data[user_id][0]

  # Increment progress (and bump tier if necessary)
  def inc_progress(self, user_id):
    self.check_init(user_id)
    self.data[user_id][0] += 1
    if self.data[user_id][0] == self.next_tier(user_id):
      self.data[user_id][1] += 1  # Bump tier
      return True
    return False

  def next_tier(self, user_id):
    self.check_init(user_id)
    tier = self.data[user_id][1]
    nt = tier + 1
    if nt >= len(self.__tiers):
      return None
    return self.__tiers[nt][0]

  def tiered_name(self, user_id):
    self.check_init(user_id)
    tier = self.data[user_id][1]
    if tier == -1:
      return self.name()
    return self.__tiers[tier][1]

  def tiered_description(self, user_id):
    self.check_init(user_id)
    tier = self.data[user_id][1]
    if tier == -1:
      return self.description()
    return self.__tiers[tier][2]

  def current_progress(self, user_id):
    res = "{}: {}".format(self.tiered_name(user_id), self.tiered_description(user_id))
    nt = self.next_tier(user_id)
    if nt is not None:
      res += " ({}/{})".format(self.progress(user_id), nt)
    return res

  def check_init(self, user_id):
    if user_id not in self.data:
      self.data[user_id] = [
         0,   # Overall progress
         -1,  # Tier
      ]
