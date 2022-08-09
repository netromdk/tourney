from .behavior import Behavior, SEASON_START_BEHAVIOR

class SeasonStartBehavior(Behavior):
  def __init__(self, user_id):
    super().__init__(SEASON_START_BEHAVIOR, user_id)
