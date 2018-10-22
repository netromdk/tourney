from .achievement import Achievement
from .behavior import INVOKE_BEHAVIOR

class ObsessedAchievement(Achievement):
  def __init__(self):
    super(ObsessedAchievement, self).__init__("Obsessed")

  def name(self):
    return "Obsessed"

  def description(self):
    return "Checked stats 10 times with !stats."

  def accepted_behaviors(self):
    return [INVOKE_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    if not user_id in self.data:
      self.data[user_id] = 0
    if behavior.command_name() == "stats":
      self.data[user_id] += 1
      return self.data[user_id] == 10
    return False

  def achieved(self, user_id):
    return user_id in self.data and self.data[user_id] >= 10
