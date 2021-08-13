from .command import Command
from tourney.teamname_generator import decorate_teamname
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
      if any([self.user_id() in t for t in teams]):
        return "{}, you are _already_ on a team today!".format(user_name)

      scored_teams = []
      for score in Scores.get().today():
        scored_teams.append(score[1])
        scored_teams.append(score[3])

      # Late-join a 1p (preferred) or 2p team
      for i in range(1, 3):
        joinable_teams = [x for x in teams if len(x) <= i and x not in scored_teams]

        if len(joinable_teams) > 0:
          new_team = choice(joinable_teams)  # nosec
          new_team_index = teams.index(new_team)

          team_name = team_names[new_team_index]

          new_team.append(self.user_id())
          new_team_name = decorate_teamname(team_name)

          teams[new_team_index] = new_team
          team_names[new_team_index] = new_team_name

          state.set_teams(teams)
          state.set_team_names(team_names)
          state.save()

          formatted_team_name = "[T{}] *{}*".format(new_team_index, team_name)

          fmt = ", ".join([lookup.user_name_by_id(uid) for uid in new_team])
          formatted_new_team_name = "[T{}] *{}*: {}".format(new_team_index, new_team_name, fmt)

          # This response must be made public because it changes the team for other players!
          self.set_public(True)

          return "{}, you've joined existing team\n{}\nwhich becomes:\n{}\n"\
            "Check `!schedule` for overview.".\
            format(user_name, formatted_team_name, formatted_new_team_name)

      return "{}, you're too late. No late-joinable teams were found.".format(user_name)
    else:
      if self.user_id() not in participants:
        state.add_participant(self.user_id())
        state.save()
        Achievements.get().interact(JoinBehavior(self.user_id()))
        return "{}, you've joined today's game!".format(user_name)
      else:
        return "{}, you've _already_ joined today's game!".format(user_name)
