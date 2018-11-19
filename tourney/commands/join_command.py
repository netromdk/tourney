from .command import Command
from tourney.constants import TEAM_NAMES, TEAM_NAME_DECORATIONS
from random import choice, shuffle

from tourney.scores import Scores
from tourney.state import State
from tourney.achievements import Achievements, JoinBehavior

class JoinCommand(Command):
  def __init__(self):
    super(JoinCommand, self).__init__("join")

  def execute(self, lookup=None):
    state = State.get()
    participants = state.participants()
    user_id = self.user_id()
    user_name = lookup.user_name_by_id(user_id)

    teams = state.teams()
    team_names = state.team_names()

    created_teams = len(teams) > 0
    if created_teams:
      joinable_teams = [x for x in teams if len(x) < 2]

      scored_teams = []
      for score in Scores.get().today():
        scored_teams.append(score[1])
        scored_teams.append(score[3])

      joinable_teams = [x for x in joinable_teams if x not in scored_teams]

      if len(joinable_teams) > 0:
        # Found a joinable team with another solo player
        new_team = choice(joinable_teams)  # nosec
        new_team_index = teams.index(new_team)

        new_team_name = team_names[new_team_index]

        new_team.append(user_id)
        new_team_name = choice(TEAM_NAME_DECORATIONS)(new_team_name)  # nosec

        teams[new_team_index] = new_team
        team_names[new_team_index] = new_team_name

        state.set_teams(teams)
        state.set_team_names(team_names)
        state.save()

        fmt = ", ".join([lookup.user_name_by_id(uid) for uid in new_team])
        formatted_team_name = "[T{}] *{}*: {}".format(new_team_index, new_team_name, fmt)

        # This response must be made public because it changes the team for other players!
        self.set_public(True)

        return "{}, you've joined existing team {}\nCheck `!schedule` for overview.".\
          format(user_name, formatted_team_name)
      else:
        # Found no joinable teams - go solo!
        new_team = [user_id]
        potential_team_names = [x for x in TEAM_NAMES if x not in team_names]
        new_team_name = choice(potential_team_names)

        teams.append(new_team)
        team_names.append(new_team_name)

        named_teams = list(zip(teams, team_names))
        shuffle(named_teams)

        teams = [nt[0] for nt in named_teams]
        team_names = [nt[1] for nt in named_teams]
        state.set_teams(teams)
        state.set_team_names(team_names)
        state.set_unrecorded_matches([])

        response = "No late-joinable teams found. {} has *GONE SOLO* on team *{}*!\n"\
            .format(user_name, new_team_name)

        # Remake schedule with the new team
        matches = []
        unrecorded_matches = []
        if len(teams) % 2 == 0:
          matches = [(i, i + 1, 2) for i in range(0, len(named_teams), 2)]
        else:
          twoRoundMatches = len(named_teams) - 3
          if twoRoundMatches > 0:
            matches = [(i, i + 1, 2) for i in range(0, len(named_teams) - 3, 2)]
          # Add last 3 matches of 1 round each.
          i = twoRoundMatches
        matches += [(i, i + 1, 1), (i, i + 2, 1), (i + 1, i + 2, 1)]
        response += "\nNew schedule:"
        for match in matches:
          plural = "s" if match[2] > 1 else ""
          name_a = named_teams[match[0]][1]
          name_b = named_teams[match[1]][1]
          response += "\n\t[T{}] *{}* vs. [T{}] *{}* ({} round{})".\
              format(match[0], name_a, match[1], name_b, match[2], plural)
          key = [match[0], match[1]]
          key.sort()
          unrecorded_matches.append(key)

        state.set_schedule(matches)
        state.set_unrecorded_matches(unrecorded_matches)
        state.save()

        # This response must be made public because it changes the schedule!
        self.set_public(True)

        return response
    else:
      if user_id not in participants:
        state.add_participant(user_id)
        state.save()
        Achievements.get().interact(JoinBehavior(user_id))
        return "{}, you've joined today's game!".format(user_name)
      else:
        return "{}, you've _already_ joined today's game!".format(user_name)
