from .command import Command

from tourney.state import State

class ScheduleCommand(Command):
  def __init__(self):
    super(ScheduleCommand, self).__init__("schedule")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    state = State.get()
    sched = state.schedule()
    teams = state.teams()
    names = state.team_names()

    if len(sched) == 0:
      return "There are no schedule yet!"

    def team_str(members):
      return ", ".join([lookup.user_name_by_id(uid) for uid in members])

    res = "Schedule:"
    for match in sched:
      plural = "s" if match[2] > 1 else ""
      name_a = names[match[0]]
      team_a = team_str(teams[match[0]])
      name_b = names[match[1]]
      team_b = team_str(teams[match[1]])
      res += "\n\t[T{}] *{}* {} vs. [T{}] *{}* {} ({} round{})".\
        format(match[0], name_a, team_a, match[1], name_b, team_b, match[2], plural)
    return res
