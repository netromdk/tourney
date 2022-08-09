from .achievement import Achievement
from .behavior import INVOKE_BEHAVIOR

class SpellingAchievement(Achievement):
  def __init__(self):
    super().__init__("Spelling")

  def name(self):
    return "I Before E"

  def description(self):
    return "Misspell \"achievement\"."

  def accepted_behaviors(self):
    return [INVOKE_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    if user_id not in self.data:
      self.data[user_id] = False
    if behavior.command_name() == "acheivements" and not self.data[user_id]:
      self.data[user_id] = True
      return True
    return False

  def achieved(self, user_id):
    return user_id in self.data and self.data[user_id]
