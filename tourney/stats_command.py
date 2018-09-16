from .command import Command
from .stats import Stats

class StatsCommand(Command):
  def __init__(self):
    super(StatsCommand, self).__init__("stats")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    stats = Stats.get()
    if not stats.generate():
      return "There are no recorded matches to generate statistics from!"

    stats.save()
    return stats.general_response(lookup)
