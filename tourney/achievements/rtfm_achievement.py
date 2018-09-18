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
    # TODO: React to whether the command is "help" or not.
    pass
