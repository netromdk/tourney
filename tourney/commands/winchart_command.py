from tourney.util import this_season_filter
from tourney.scores import Scores

from .command import Command

class WinChartCommand(Command):
  def __init__(self, client):
    super(WinChartCommand, self).__init__("winchart")
    self.client = client
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    scores = Scores.get()
    # TODO: DM personalized wincharts
    winrate_plot = scores.get_season_winrate_plot(time_filter=this_season_filter,
                                                  lookup=lookup)
    if winrate_plot is None:
      return "Not enough season data!"
    else:
      try:
        with open(winrate_plot, mode="rb") as file_content:
          self.client.api_call(
            "files.upload",
            channels=self.channel(),
            file=file_content,
            initial_comment="Win percentage progression for the current season",
            title="Season win progression"
          )
          return "Win percentage progression for the current season"
      except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        return "Could not open generated winchart"
