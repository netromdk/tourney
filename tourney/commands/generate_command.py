from tourney.state import State
from tourney.match_scheduling import create_teams, create_schedule, schedule_text
from tourney.constants import MATCHMAKING
from tourney.teams import Teams

from random import random

from .command import Command

class GenerateCommand(Command):
  def __init__(self):
    super(GenerateCommand, self).__init__("stats")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    state = State.get()
    response = "<!channel>\n"
    teams, names = create_teams()

    if teams is None:
      response += "No games possible! At least 2 players are required!"
    else:
      # Whether or not to do matchmaking or random matchups.
      if not MATCHMAKING:
        rand_matches = True
      else:
        # 50% chance of random. Range is [0.0, 1.0)
        rand_matches = random() < 0.5  # nosec

      sched = create_schedule(teams, rand_matches)
      unrecorded_matches = []
      for match in sched:
        key = [match[0], match[1]]
        key.sort()
        unrecorded_matches.append(key)

      # Remember teams and unrecorded matches but clear participants, morning announce, and users that
      # didn't want today's reminder.
      state.set_schedule(sched)
      state.set_teams(teams)
      state.set_team_names(names)
      state.set_unrecorded_matches(unrecorded_matches)

      if len(teams) > 3 and rand_matches:
        response += ":tractor::dash: {} :tractor::dash:\n\n".\
          format("Today's matchups brought to you by the RANDOM FACTOR TRACTOR")

      # Generate response for the channel.
      response += schedule_text(lookup)

      tteams = Teams.get()
      (gen2p, gen3p) = tteams.get_regenerated_users()
      regen_set = set(gen2p + gen3p)
      if len(regen_set) > 0:
        response += "\n\n:recycle: Regenerated teams for:\n"
        for p in regen_set:
          response += "  {}\n".format(lookup.user_name_by_id(p))

    # Clean state
    state.set_participants([])
    state.set_morning_announce(None)
    state.set_dont_remind_users([])
    state.save()
    
    return response
