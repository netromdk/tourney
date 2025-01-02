from random import choice
import itertools

from tourney.teamname_generator import decorate_teamname
from tourney.scores import Scores
from tourney.state import State
from tourney.achievements import Achievements, JoinBehavior
from tourney.util import decorated_playername_list
from tourney.match_scheduling import create_matches

from .command import Command

class JoinCommand(Command):
  def __init__(self):
    super().__init__("join")

  def execute(self, lookup=None):
    state = State.get()
    participants = state.participants()
    user_name = lookup.user_name_by_id(self.user_id())

    teams = state.teams()
    team_names = state.team_names()

    created_teams = len(teams) > 0
    if created_teams:
      if any(self.user_id() in t for t in teams):
        return "{}, you are _already_ on a team today!".format(user_name)

      scored_teams = []
      for score in Scores.get().today():
        scored_teams.append(score[1])
        scored_teams.append(score[3])

      if len(scored_teams) > 0:
        return "Sorry, {}, you cannot join after matches have been scored.".format(user_name)

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

          plist = decorated_playername_list(new_team, lookup)
          formatted_new_team_name = "[T{}] *{}*: {}".\
            format(new_team_index, new_team_name, ", ".join(plist))

          # This response must be made public because it changes the team for other players!
          self.set_public(True)

          return "{}, you've joined existing team\n{}\nwhich becomes:\n{}\n"\
            "Check `!schedule` for overview.".\
            format(user_name, formatted_team_name, formatted_new_team_name)

      # No joinable teams found - create new schedule!
      # Flatten teams lists.
      state.set_participants(list(itertools.chain.from_iterable(state.teams())) + [self.user_id()])

      state.set_teams([])
      state.set_team_names([])
      state.set_schedule([])
      state.set_unrecorded_matches([])

      response = "No teams available for {} to late-join! "\
        "Regenerating all matches.\n".format(user_name)
      response += create_matches(lookup)

      return response

    if self.user_id() not in participants:
      state.add_participant(self.user_id())
      state.save()
      Achievements.get().interact(JoinBehavior(self.user_id()))
      return "{}, you've joined today's game!".format(user_name)

    return "{}, you've _already_ joined today's game!".format(user_name)
