from .behavior import Behavior, NAME_TEAM_BEHAVIOR

class NameTeamBehavior(Behavior):
  def __init__(self, user_id):
    super(NameTeamBehavior, self).__init__(NAME_TEAM_BEHAVIOR, user_id)
