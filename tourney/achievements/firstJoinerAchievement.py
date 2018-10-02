from .achievement import Achievement
from .behavior import JOIN_BEHAVIOR
from tourney.state import State

class FirstJoinerAchievement(Achievement):
  def __init__(self):
    super(FirstJoinerAchievement, self).__init__("FirstJoiner")

  def name(self):
    return "Early Bird"

  def description(self):
    return "Be the first player to join the game of the day"

  def accepted_behaviors(self):
    return [JOIN_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    state = State.get()
    participants = state.participants()
    if len(participants) == 1:
      self.data[user_id][1] = True
      return True
    return False

  def achieved(self, user_id):
    return user_id in self.data and self.data[user_id]

  def progress(self, user_id):
    return 0

  def next_tier(self, user_id):
    return None

  def tiered_name(self, user_id):
    return self.Name()

  def tiered_description(self, user_id):
    return self.description()
