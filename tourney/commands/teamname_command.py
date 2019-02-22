from .command import Command

from tourney.teamnames import Teamnames
from tourney.state import State
from tourney.scores import Scores

class TeamnameCommand(Command):
  def __init__(self):
    super(TeamnameCommand, self).__init__("teamname")

  def execute(self, lookup=None):
    state = State.get()
    teamnames = Teamnames.get()

    current_teams = state.teams()
    current_teamnames = state.team_names()

    my_teams = []
    if len(current_teams) == 0:
      scores = Scores.get()
      matches_today = scores.today()
      for m in matches_today:
        if self.user_id() in m[1]:
          my_teams.append(m[1])
        if self.user_id() in m[3]:
          my_teams.append(m[3])
    else:
      my_teams = [x for x in current_teams if self.user_id() in x]

    response = ""

    if len(my_teams) == 0:
      response = "You can't claim a team name if you aren't on a team!"
      return response

    if len(my_teams) > 1:
      response = "Cannot assign team name when player appears in multiple teams."
      return response

    teamname = self.args()

    if len(teamname) == 0:
      response = "Please provide a new team name, e.g. \"!teamname Example Team Name\""
      return response

    my_team = my_teams[0]
    team_idx = current_teams.index(my_team)

    teamnames.add(my_team, teamname)
    teamnames.save()

    current_teamnames[team_idx] = teamname
    state.set_team_names(current_teamnames)
    state.save()

    # Prepend ", " or " and " before all non-first entries
    amount = len(my_team)
    for idx in range(amount):
      if idx > 0:
        if idx == amount - 1:
          if amount > 2:
            response += ","
          response += " and "
        else:
          response += ", "
      response += lookup.user_name_by_id(my_team[idx])

    response += " will henceforth be known as {}".format(teamname)
    return response
