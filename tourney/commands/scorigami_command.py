from .command import Command

from tourney.scores import Scores

class ScorigamiCommand(Command):
  def __init__(self):
    super(ScorigamiCommand, self).__init__("scorigami")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    scores = Scores.get()

    scorigami_plot = scores.get_scorigami_plot()

    return scorigami_plot
