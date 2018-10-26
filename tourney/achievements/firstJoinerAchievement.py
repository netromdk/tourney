from .achievement import Achievement
from .behavior import JOIN_BEHAVIOR
from tourney.state import State

class FirstJoinerAchievement(Achievement):
  def __init__(self):
    super(FirstJoinerAchievement, self).__init__("FirstJoiner")

  def name(self):
    return "Early Bird"

  def description(self):
    return "Be the first player to join the game of the day."

  def accepted_behaviors(self):
    return [JOIN_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    state = State.get()
    participants = state.participants()
    if not user_id in self.data:
      self.data[user_id] = False
    if len(participants) == 1:
      self.data[user_id] = True
      return True
    return False

  def achieved(self, user_id):
    return user_id in self.data and self.data[user_id]
