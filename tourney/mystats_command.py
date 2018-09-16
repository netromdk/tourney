from .command import Command
from .stats import Stats

class MyStatsCommand(Command):
  def __init__(self):
    super(MyStatsCommand, self).__init__("mystats")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    stats = Stats.get()
    if not stats.generate():
      return "There are no recorded matches to generate statistics from!"

    stats.save()
    return stats.personal_response(lookup, self.user_id())
