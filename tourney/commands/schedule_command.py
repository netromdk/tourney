from .command import Command

from tourney.state import State
from tourney.scores import Scores

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

    scores = Scores.get()
    played = scores.today()

    def team_str(members):
      return ", ".join([lookup.user_name_by_id(uid) for uid in members])

    res = "Schedule:"
    for match in sched:
      plural = "s" if match[2] > 1 else ""
      name_a = names[match[0]]
      team_a = teams[match[0]]
      team_a_str = team_str(team_a)
      team_a_score = None
      name_b = names[match[1]]
      team_b = teams[match[1]]
      team_b_str = team_str(team_b)
      team_b_score = None

      # Check if match was already played.
      for pm in played:
        if (pm[1] == team_a or pm[1] == team_b) and (pm[3] == team_a or pm[3] == team_b):
          if pm[1] == team_a:
            team_a_score = pm[2]
            team_b_score = pm[4]
          else:
            team_a_score = pm[4]
            team_b_score = pm[2]
          break

      res += "\n\t[T{}] *{}*: {}".format(match[0], name_a, team_a_str)
      if team_a_score is not None:
        res += " *({} pts)*".format(team_a_score)

      res += " vs. [T{}] *{}*: {}".format(match[1], name_b, team_b_str)
      if team_b_score is not None:
        res += " *({} pts)*".format(team_b_score)

      res += " ({} round{})".format(match[2], plural)
    return res
