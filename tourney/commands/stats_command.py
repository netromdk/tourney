from .command import Command

from datetime import datetime
import calendar
from tourney.util import this_season_filter

from tourney.stats import Stats

class StatsCommand(Command):
  def __init__(self):
    super(StatsCommand, self).__init__("stats")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    stats = Stats.get()

    if not stats.generate(time_filter=this_season_filter):
      return "There are no recorded matches to generate statistics from!"

    stats.save()
    month = calendar.month_name[datetime.today().month]

    return "Statistics for the {} season:\n".format(month) + stats.general_response(lookup)
