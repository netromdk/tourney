from .achievement import Achievement
from .behavior import INVOKE_BEHAVIOR

class RtfmAchievement(Achievement):
  def __init__(self):
    super(RtfmAchievement, self).__init__("RTFM")

  def name(self):
    return "RTFM"

  def description(self):
    return "Use the !help command."

  def accepted_behaviors(self):
    return [INVOKE_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    if not user_id in self.data:
      self.data[user_id] = False
    if behavior.command_name() == "help" and not self.data[user_id]:
      self.data[user_id] = True
      return True
    return False

  def achieved(self, user_id):
    return user_id in self.data and self.data[user_id]
