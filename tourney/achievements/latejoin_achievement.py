from tourney.state import State

from .tiered_achievement import TieredAchievement
from .behavior import JOIN_BEHAVIOR

class LateJoinAchievement(TieredAchievement):
  def __init__(self):
    print("late join init")
    tiers = (
      (1,   "Fashionably Late",
       "Join after teams have been generated."),
      (5,   "Slowpoke",
       "Miss the team generation deadline 5 times"),
      (10,  "Columbo",
       "Adding just one more player to the lineup, ten times."),
      (25,  "Sloth Incarnate",
       "Show a complete disregard for deadlines twenty five times."),
      (50,  "Gandalf",
       "A foosballer is never late, nor are they early. "
       "They join precisely when they mean to. Fifty times."),
    )
    super().__init__("LateJoiner", tiers)

  def accepted_behaviors(self):
    return [JOIN_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    state = State.get()

    teams = state.teams()
    if len(teams) > 0 and not all(user_id in t for t in teams):
      if self.inc_progress(user_id):
        return True

    return False
