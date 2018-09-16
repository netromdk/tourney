from .command import Command
from .constants import POSITIVE_REACTIONS, NEGATIVE_REACTIONS

class HelpCommand(Command):
  def __init__(self):
    super(HelpCommand, self).__init__("help")

  def execute(self):
    return """
As the foosball bot, I accept the following commands:
  `!help` - Shows this text.
  `!list` - List users that joined game of the day.
  `!join` or positive reaction - Join game of the day.
  `!leave` or negative reaction - Leave game of the day.
  `!win` - Add match scores (irrelevant order) as a member of the winning team. Example: `!win 8 3`
  `!lose` - Add match scores (irrelevant order) as a member of the losing team. Example: `!lose 8 3`
  `!score` - Add match scores of two teams. Example: `!score T0 12 T3 16`
  `!stats` - Prints general statistics of all games.
  `!mystats` - Prints statistics of all games about invoker.
  `!undoteams` - Undoes teams and matches and restores as players joined. (*privileged!*)
  `!generate` - Generate teams and matches from players joined. (*privileged!*)
  `!autoupdate` - Updates project git repo and restarts bot. (*privileged!*)

Positive reactions: {}
Negative reactions: {}
""".format(" ".join([":{}:".format(r) for r in POSITIVE_REACTIONS]),
           " ".join([":{}:".format(r) for r in NEGATIVE_REACTIONS]))
