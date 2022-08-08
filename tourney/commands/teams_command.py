from tourney.state import State

from .command import Command

class TeamsCommand(Command):
  def __init__(self):
    super(TeamsCommand, self).__init__("teams")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    state = State.get()
    teams = state.teams()
    names = state.team_names()

    if len(teams) == 0:
      return "There are no teams created yet!"

    res = "{} teams: ".format(len(teams))
    for i in range(len(teams)):
      fmt = ", ".join([lookup.user_name_by_id(uid) for uid in teams[i]])
      name = names[i]
      res += "\n\t[T{}] *{}*: {}".format(i, name, fmt)
    return res
