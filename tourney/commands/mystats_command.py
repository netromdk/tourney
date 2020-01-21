from .command import Command

from tourney.constants import STATS_PLACEMENT_DELTA
from tourney.util import this_season_filter, to_ordinal
from tourney.stats import Stats
from tourney.player_skill import PlayerSkill

class MyStatsCommand(Command):
  def __init__(self):
    super(MyStatsCommand, self).__init__("mystats")

  def execute(self, lookup=None):
    user_id = self.user_id()
    stats = Stats.get()
    if not stats.generate():
      return "There are no recorded matches to generate statistics from!"

    stats.save()
    response = stats.personal_response(lookup, user_id)

    # Generate a local top 5 around this users position in the ranking
    if stats.generate(time_filter=this_season_filter):
      stats.save()
      response += stats.local_top_list(user_id, STATS_PLACEMENT_DELTA, lookup)

    ps = PlayerSkill.get()
    rank = ps.get_player_rank(user_id)
    place = to_ordinal(ps.get_player_placement(user_id))

    response += "\nYour TrueSkill rank is currently {:.2f}, which puts you in {} place.\n".\
      format(rank, place)

    return response
