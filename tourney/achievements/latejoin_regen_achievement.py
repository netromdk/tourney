from tourney.state import State
from tourney.scores import Scores

from .tiered_achievement import TieredAchievement
from .behavior import JOIN_BEHAVIOR

class LateJoinRegenerateAchievement(TieredAchievement):
  def __init__(self):
    tiers = (
      (1,   "Deal Breaker",
       "Force a regeneration of teams by joining late."),
      (5,   "Party Crasher",
       "Force regeneration of teams by inexplicably joining late 5 times."),
      (10,  "Agent of Chaos",
       "With complete disregard for punctuality, "
       "force regeneration of teams by joining late 10 times!")
    )
    super().__init__("LateJoinRegenerate", tiers)

  def accepted_behaviors(self):
    return [JOIN_BEHAVIOR]

  def update(self, behavior):
    user_id = behavior.user_id()
    state = State.get()
    teams = state.teams()
    if len(teams) == 0:
      return False  # No teams

    if any(user_id in t for t in teams):
      return False  # Already on a team

    scored_teams = []
    for score in Scores.get().today():
      scored_teams.append(score[1])
      scored_teams.append(score[3])

    if len(scored_teams) > 0:
      return False  # Cannot late join after first score

    if not any(len(t) < 3 and t not in scored_teams for t in teams):
      # No late join team available - regeneration
      if self.inc_progress(user_id):
        return True

    # Joined an existing team
    return False
