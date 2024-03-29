from tourney.stats import Stats

from .command import Command

class AllStatsCommand(Command):
  def __init__(self):
    super().__init__("allstats")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    stats = Stats.get()
    if not stats.generate():
      return "There are no recorded matches to generate statistics from!"

    stats.save()
    return "All time statistics:" + stats.general_response(lookup)
