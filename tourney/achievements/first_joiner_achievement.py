from tourney.state import State

from .tiered_achievement import TieredAchievement
from .behavior import JOIN_BEHAVIOR

class FirstJoinerAchievement(TieredAchievement):
  def __init__(self):
    tiers = (
      (1,   "Early Bird",    "Be the first player to join the game of the day."),
      (5,   "Earlier Bird",  "Be the first player to join five times."),
      (10,  "Earliest Bird", "Be the first player to join ten times."),
      (25,  "Night Owl",     "Be the first player to join twenty five times."),
      (50,  "Pterosaur",     "Earliest of the birds! Be the first player to join fifty times."),
    )
    super().__init__("FirstJoiner", tiers)

  def achieved(self, user_id):
    self.convert_from_untiered(user_id)
    self.check_init(user_id)
    return self.data[user_id][1] >= 0

  def accepted_behaviors(self):
    return [JOIN_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    state = State.get()
    participants = state.participants()

    if user_id in self.data:
      self.convert_from_untiered(user_id)

    if len(participants) == 1:
      if self.inc_progress(user_id):
        return True

    return False
