from tourney.achievements import Achievements

from .command import Command

class AchievementsCommand(Command):
  def __init__(self):
    super(AchievementsCommand, self).__init__("achievements")

  def execute(self, lookup=None):
    achievements = Achievements.get()
    return achievements.user_response(self.user_id())
