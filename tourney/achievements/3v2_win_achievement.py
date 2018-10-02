from .achievement import Achievement
from .behavior import WIN_BEHAVIOR

class 3v2WinAchievement(Achievement):
  def __init__(self):
    super(3v2WinAchievement, self).__init__("3v2Win")

  def name(self):
    return "Strength in Numbers"

  def description(self):
    return "In a three-player team, beat a two player team"

  def accepted_behaviors(self):
    return [WIN_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    user_team = behavior.winner_team()
    loser_team = behavior.loser_team()
    if len(user_team) == 3 and len(loser_team) == 2:
      self.data[user_id] = True
      return True
    return False

  def achieved(self, user_id):
    return user_id in self.data and self.data[user_id]

  def progress(self, user_id):
    return 0

  def next_tier(self, user_id):
    return None

  def tiered_name(self, user_id):
    return self.name()

  def tiered_description(self, user_id):
    return self.description()
