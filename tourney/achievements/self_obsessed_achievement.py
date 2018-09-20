from .achievement import Achievement
from .behavior import INVOKE_BEHAVIOR

class SelfObsessedAchievement(Achievement):
  def __init__(self):
    super(SelfObsessedAchievement, self).__init__("SelfObsessed")

  def name(self):
    return "Self-Obsessed"

  def description(self):
    return "Checked own stats 10 times with !mystats."

  def accepted_behaviors(self):
    return [INVOKE_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    if not user_id in self.data:
      self.data[user_id] = 0
    if behavior.command_name() == "mystats":
      self.data[user_id] += 1
      return self.data[user_id] == 10
    return False

  def achieved(self, user_id):
    return user_id in self.data and self.data[user_id] >= 10

  def progress(self, user_id):
    return 0

  def next_tier(self, user_id):
    return None

  def tiered_name(self, user_id):
    return self.name()

  def tiered_description(self, user_id):
    return self.description()
