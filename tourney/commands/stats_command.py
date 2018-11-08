from .command import Command

from datetime import timedelta

from tourney.stats import Stats
from tourney.constants import STATS_DAYS_BACK

class StatsCommand(Command):
  def __init__(self):
    super(StatsCommand, self).__init__("stats")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    stats = Stats.get()

    if not stats.generate(timedelta(days=STATS_DAYS_BACK)):
      return "There are no recorded matches to generate statistics from!"

    stats.save()
    return "Statistics going back {} days:".format(STATS_DAYS_BACK) + stats.general_response(lookup)
