from .command import Command

import re

from tourney.state import State
from tourney.scores import Scores
from tourney.player_skill import PlayerSkill
from tourney.constants import WIN_ARGS_REGEX
from tourney.achievements import Achievements, WinBehavior, LoseBehavior, ReportScoreBehavior
from tourney.util import schedule_text

class WinLoseCommand(Command):
  def __init__(self, name):
    super(WinLoseCommand, self).__init__(name)
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    win = self.name() == "win"
    state = State.get()
    teams = state.teams()
    names = state.team_names()
    unrecorded_matches = state.unrecorded_matches()
    if len(teams) == 0:
      return "Cannot report scores when no teams have been created!"

    example = "`!{} 12 16`".format(self.name())
    m = re.match(WIN_ARGS_REGEX, self.args())
    if not m:
      return "Requires arguments for scores! Like {}".format(example)

    scores_arg = list(map((int), m.groups()))
    winIndex = scores_arg.index(max(scores_arg))
    loseIndex = scores_arg.index(min(scores_arg))
    if win:
      myScore = scores_arg[winIndex]
      theirScore = scores_arg[loseIndex]
    else:
      myScore = scores_arg[loseIndex]
      theirScore = scores_arg[winIndex]

    rounds = max(scores_arg) // 8

    response = ""
    if (myScore >= 0 and theirScore >= 0) and (myScore % 8 == 0 or theirScore % 8 == 0):
      myTeams = [x for x in teams if self.user_id() in x]
      if len(myTeams) == 1:
        myTeam = myTeams[0]
        myTeamIndex = teams.index(myTeam)
        myTeamName = names[myTeamIndex]
        myMatches = [x for x in unrecorded_matches if myTeamIndex in x]
        if len(myMatches) == 1:
          myMatch = myMatches[0]
          theirTeamIndex = myMatch[(myMatch.index(myTeamIndex) + 1) % 2]
          theirTeam = teams[theirTeamIndex]
          theirTeamName = names[theirTeamIndex]

          unrecorded_matches.remove(myMatch)
          state.set_unrecorded_matches(unrecorded_matches)
          state.save()

          if win:
            win_team = myTeam
            win_score = myScore
            lose_team = theirTeam
            lose_score = theirScore
          else:
            win_team = theirTeam
            win_score = theirScore
            lose_team = myTeam
            lose_score = myScore

          player_skill = PlayerSkill.get()
          player_skill.rate_match(win_team, lose_team)
          player_skill.save()

          scores = Scores.get()

          scorigami = scores.get_scorigami(win_score, lose_score)

          scores.add(myTeam, myScore, theirTeam, theirScore)
          scores.save()

          achievements = Achievements.get()
          for member in win_team:
            achievements.interact(WinBehavior(member, rounds, win_score, lose_score, win_team,
                                              lose_team))
          for member in lose_team:
            achievements.interact(LoseBehavior(member, rounds, win_score, lose_score))

          achievements.interact(ReportScoreBehavior(self.user_id(), win_team, lose_team))

          response = "Added scores for [T{}] *{}* ({} pts) v [T{}] *{}* ({} pts)!".\
            format(myTeamIndex, myTeamName, myScore, theirTeamIndex, theirTeamName, theirScore)

          if scorigami[0] == 0:
            response += "\n:rotating_light:That's Scorigami!:rotating_light:"
          else:
            response += "\nNo Scorigami. That score has happened {} times before, "\
              "last time on {}/{}/{}".\
              format(scorigami[0], scorigami[1].day, scorigami[1].month, scorigami[1].year)

          rem = len(unrecorded_matches)
          if rem == 0:
            response += "\nNo more matches left to record!"
          else:
            response += "\n{} matches left to record!".format(rem)
          response += "\n{}".format(schedule_text(lookup, True))
        elif len(myMatches) > 1:
          response = "You appear in multiple matches. Please use explicit scoring with !score."
        else:
          response = "Found no unscored matches with you as a player."
      else:
        response = "You do not appear in any teams."
    else:
      response = "Scores must be positive and one be divisible by 8."

    return response
