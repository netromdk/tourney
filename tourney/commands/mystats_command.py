from .command import Command
from tourney.constants import STATS_PLACEMENT_DELTA

from datetime import datetime
import calendar
from tourney.util import this_season_filter

from tourney.stats import Stats

class MyStatsCommand(Command):
  def __init__(self):
    super(MyStatsCommand, self).__init__("mystats")

  def execute(self, lookup=None):
    user_id = self.user_id()
    stats = Stats.get()
    if not stats.generate():
      return "There are no recorded matches to generate statistics from!"

    stats.save()
    response = stats.personal_response(lookup, user_id)

    # Generate a local top 5 around this users position in the ranking
    if stats.generate(time_filter=this_season_filter):
      stats.save()
      response += stats.local_top_list(user_id, STATS_PLACEMENT_DELTA)

    return response
