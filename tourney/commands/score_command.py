import re

from .command import Command

from tourney.state import State
from tourney.constants import SCORE_ARGS_REGEX
from tourney.scores import Scores
from tourney.player_skill import PlayerSkill
from tourney.achievements import Achievements, WinBehavior, LoseBehavior, ReportScoreBehavior
from tourney.util import schedule_text

class ScoreCommand(Command):
  def __init__(self):
    super(ScoreCommand, self).__init__("score")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    state = State.get()
    teams = state.teams()
    names = state.team_names()
    unrecorded_matches = state.unrecorded_matches()
    user_id = self.user_id()

    if len(teams) == 0:
      return "Cannot report scores when no teams have been created!"

    example = "`!score T0 12 T3 16`"
    m = re.match(SCORE_ARGS_REGEX, self.args())
    if not m:
      return "Requires arguments for teams and scores! Like {}".format(example)

    team_a = int(m.group(1)[1:])
    team_a_score = int(m.group(2))
    team_a_name = names[team_a]
    team_b = int(m.group(3)[1:])
    team_b_score = int(m.group(4))
    team_b_name = names[team_b]
    r = range(len(teams))

    rounds = max([team_a_score, team_b_score]) // 8

    response = None
    if team_a in r and team_b in r and team_a_score >= 0 and team_b_score >= 0 and \
       (team_a_score % 8 == 0 or team_b_score % 8 == 0):
      key = [team_a, team_b]
      key.sort()
      if key in unrecorded_matches:
        ids_a = teams[team_a]
        ids_b = teams[team_b]
        if user_id in ids_a or user_id in ids_b:
          unrecorded_matches.remove(key)
          state.set_unrecorded_matches(unrecorded_matches)
          state.save()

          scores = Scores.get()
          scores.add(ids_a, team_a_score, ids_b, team_b_score)
          scores.save()

          if team_a_score > team_b_score:
            win_team = ids_a
            win_score = team_a_score
            lose_team = ids_b
            lose_score = team_b_score
          else:
            win_team = ids_b
            win_score = team_b_score
            lose_team = ids_a
            lose_score = team_a_score

          player_skill = PlayerSkill.get()
          player_skill.rate_match(win_team, lose_team)
          player_skill.save()

          achievements = Achievements.get()
          for member in win_team:
            achievements.interact(WinBehavior(member, rounds, win_score, lose_score, win_team,
                                              lose_team))
          for member in lose_team:
            achievements.interact(LoseBehavior(member, rounds, win_score, lose_score))

          achievements.interact(ReportScoreBehavior(self.user_id(), win_team, lose_team))

          response = "Added scores for [T{}] *{}* ({} pts) v [T{}] *{}* ({} pts)!".\
            format(team_a, team_a_name, team_a_score, team_b, team_b_name, team_b_score)
          rem = len(unrecorded_matches)
          if rem == 0:
            response += "\nNo more matches left to record!"
          else:
            response += "\n{} matches left to record!".format(rem)
          response += "\n{}".format(schedule_text(lookup, True))
        else:
          response = "Only players of a match can report the score!"
      else:
        response = "Match has already been recorded or isn't scheduled!"

    if response is None:
      response = """
Invalid arguments!
Teams must be input like 'T1' and scores must be positive and one be divisible by 8.
Example: {}
""".format(example)

    return response
