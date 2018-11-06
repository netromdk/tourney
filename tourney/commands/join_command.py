from .command import Command
from tourney.constants import TEAM_NAME_DECORATIONS
from random import shuffle, choice

from tourney.state import State
from tourney.achievements import Achievements, JoinBehavior

class JoinCommand(Command):
  def __init__(self):
    super(JoinCommand, self).__init__("join")

  def execute(self, lookup=None):
    state = State.get()
    participants = state.participants()
    user_name = lookup.user_name_by_id(self.user_id())

    teams = state.teams()
    teamNames = state.team_names()

    created_teams = len(teams) > 0
    if created_teams:
      matches = state.unrecorded_matches()
      teams_with_matches = []
      for match in matches:
        if not match[0] in teams_with_matches:
          teams_with_matches.append(match[0])
        if not match[1] in teams_with_matches:
          teams_with_matches.append(match[1])

      joinable_teams = [teamIdx for teamIdx in teams_with_matches if len(teams[teamIdx]) == 2]

      if len(joinable_teams) > 0:
        shuffle(joinable_teams)
        new_team_index = joinable_teams[0]
        new_team = teams[new_team_index]
        new_team_name = teamNames[new_team_index]

        new_team.append(self.user_id())
        new_team_name = choice(TEAM_NAME_DECORATIONS)(new_team_name)

        teams[new_team_index] = new_team
        teamNames[new_team_index] = new_team_name

        state.set_teams(teams)
        state.set_team_names(teamNames)

        fmt = ", ".join([lookup.user_name_by_id(uid) for uid in new_team])
        formatted_team_name = "[T{}] *{}*: {}".format(new_team_index, new_team_name, fmt)
        return "{}, you've joined existing team {}\n".format(user_name, formatted_team_name)
      else:
        return "{}, you're too late. No late-joinable teams were found.".format(user_name)
    else:
      if self.user_id() not in participants:
        state.add_participant(self.user_id())
        state.save()
        Achievements.get().interact(JoinBehavior(self.user_id()))
        return "{}, you've joined today's game!".format(user_name)
      else:
        return "{}, you've _already_ joined today's game!".format(user_name)
