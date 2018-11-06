from .command import Command
from tourney.constants import TEAM_NAME_DECORATIONS
from random import choice

from tourney.scores import Scores
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
    team_names = state.team_names()

    created_teams = len(teams) > 0
    if created_teams:
      joinable_teams = [x for x in teams if len(x) == 2]

      scored_teams = []
      for score in Scores.get().today():
        scored_teams.append(score[1])
        scored_teams.append(score[3])

      joinable_teams = [x for x in joinable_teams if x not in scored_teams]

      if len(joinable_teams) > 0:
        new_team = choice(joinable_teams)  # nosec
        new_team_index = teams.index(new_team)

        new_team_name = team_names[new_team_index]

        new_team.append(self.user_id())
        new_team_name = choice(TEAM_NAME_DECORATIONS)(new_team_name)  # nosec

        teams[new_team_index] = new_team
        team_names[new_team_index] = new_team_name

        state.set_teams(teams)
        state.set_team_names(team_names)

        fmt = ", ".join([lookup.user_name_by_id(uid) for uid in new_team])
        formatted_team_name = "[T{}] *{}*: {}".format(new_team_index, new_team_name, fmt)
        return "{}, you've joined existing team {}".format(user_name, formatted_team_name)
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
