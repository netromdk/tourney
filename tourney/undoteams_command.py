import itertools

from .command import Command
from .state import State

class UndoTeamsCommand(Command):
  def __init__(self):
    super(UndoTeamsCommand, self).__init__("undoteams")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    state = State.get()
    if len(state.teams()) == 0:
      return "No teams and matches to dissolve!"

    # Flatten teams lists.
    state.set_participants(list(itertools.chain.from_iterable(state.teams())))

    state.set_teams([])
    state.set_team_names([])
    state.set_unrecorded_matches([])
    state.set_midday_announce(False)
    state.save()

    return "Games have been canceled, teams dissolved, and all players are on the market again!"
