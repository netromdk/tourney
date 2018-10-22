from .achievement import Achievement
from .behavior import WIN_BEHAVIOR

class ThreeVTwoWinAchievement(Achievement):
  def __init__(self):
    super(ThreeVTwoWinAchievement, self).__init__("ThreeVTwoWin")

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
