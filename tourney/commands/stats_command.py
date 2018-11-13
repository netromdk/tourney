from .command import Command

from datetime import datetime
import calendar

from tourney.stats import Stats

class StatsCommand(Command):
  def __init__(self):
    super(StatsCommand, self).__init__("stats")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    stats = Stats.get()

    def this_month_filter(time_stamp):
      return datetime.fromtimestamp(time_stamp).month == datetime.today().month

    if not stats.generate(time_filter=this_month_filter):
      return "There are no recorded matches to generate statistics from!"

    stats.save()
    month = calendar.month_name[datetime.today().month]

    return "Statistics for {}:".format(month) + stats.general_response(lookup)
