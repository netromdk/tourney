from tourney.match_scheduling import create_matches

from .command import Command

class GenerateCommand(Command):
  def __init__(self):
    super(GenerateCommand, self).__init__("stats")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    return create_matches(lookup)
