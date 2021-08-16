from .command import Command

from tourney.constants import POSITIVE_REACTIONS, NEGATIVE_REACTIONS

class HelpCommand(Command):
  def __init__(self):
    super(HelpCommand, self).__init__("help")

  def execute(self, lookup=None):
    return """
As the foosball bot, I accept the following commands:
  `!help` - Shows this text.
  `!list` - List users that joined game of the day.
  `!join` or positive reaction - Join game of the day.
  `!leave` or negative reaction - Leave game of the day.
  `!teams` - Prints teams of today's matches.
  `!schedule` - Prints schedule of the day.
  `!win` - Add match scores (irrelevant order) as a member of the winning team. Example: `!win 8 3`
  `!lose` - Add match scores (irrelevant order) as a member of the losing team. Example: `!lose 8 3`
  `!score` - Add match scores of two teams. Example: `!score T0 12 T3 16`
  `!results` - Prints results of today's matches.
  `!stats` - Prints general statistics for the current season.
  `!allstats` - Prints general statistics of all games.
  `!mystats` - Prints statistics of all games about invoker.
  `!achievements` - Prints achievements progress for invoker.
  `!teamname` - Set a team name for your team.
                Call without argument to claim your current team name.
                Claim the teamname you already have to "forget" it instead.
                Example: `!teamname Example Name`
  `!undoteams` - Undoes teams and matches and restores as players joined. (*privileged!*)
  `!generate` - Generate teams and matches from players joined. (*privileged!*)
  `!autoupdate` - Updates project git repo and restarts bot. (*privileged!*)
  `!startseason` - Starts a new season. (*privileged!*)

Positive reactions: {}
Negative reactions: {}
""".format(" ".join([":{}:".format(r) for r in POSITIVE_REACTIONS]),
           " ".join([":{}:".format(r) for r in NEGATIVE_REACTIONS]))
