from .command import Command

from tourney.teamnames import Teamnames
from tourney.state import State

class TeamnameCommand(Command):
  def __init__(self):
    super(TeamnameCommand, self).__init__("teamname")

  def execute(self, lookup=None):
    state = State.get()
    teamnames = Teamnames.get()

    current_teams = state.teams()
    current_teamnames = state.team_names()

    my_teams = [x for x in current_teams if self.user_id() in x]

    response = ""
    print(my_teams)

    if len(my_teams) == 0:
      response = "No team found."
      return response

    if len(my_teams) > 1:
      response = "Cannot assign teamname when player appears in multiple teams."
      return response

    teamname = self.args()

    if len(teamname) == 0:
      response = "Please provide a new teamname, e.g. \"!teamname Example Teamname\""
      return response

    my_team = my_teams[0]
    old_teamname_idx = current_teams.index(my_team)

    teamnames.add(my_team, teamname)
    teamnames.save()

    current_teamnames[old_teamname_idx] = teamname
    state.set_team_names(current_teamnames)
    state.save()

    if len(my_team) == 1:
      user_name = lookup.user_name_by_id(my_team[0])
      response += user_name
    elif len(my_team) == 2:
      user_name1 = lookup.user_name_by_id(my_team[0])
      user_name2 = lookup.user_name_by_id(my_team[1])
      response += "{} and {}".format(user_name1, user_name2)
    elif len(my_team) == 3:
      user_name1 = lookup.user_name_by_id(my_team[0])
      user_name2 = lookup.user_name_by_id(my_team[1])
      user_name3 = lookup.user_name_by_id(my_team[2])
      response += "{}, {} and {}".format(user_name1, user_name2, user_name3)
    else:
      response += "[{}".format(lookup.user_name_by_id(my_team[0]))
      for id in my_team[1:]:
        response += ", {}".format(lookup.user_name_by_id(id))
      response += "]"

    response += " will henceforth be known as {}".format(teamname)
    return response
