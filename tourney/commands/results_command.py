from .command import Command

from tourney.scores import Scores

class ResultsCommand(Command):
  def __init__(self):
    super(ResultsCommand, self).__init__("results")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    matches = Scores.get().today()
    if len(matches) == 0:
      return "No recorded matches of today."

    def team_str(members):
      return ", ".join([lookup.user_name_by_id(uid) for uid in members])

    res = ["Results of today:"]
    for m in matches:
      t0 = team_str(m[1])
      t0_score = m[2]
      t1 = team_str(m[3])
      t1_score = m[4]
      if t0_score < t1_score:
        t0, t1 = t1, t0
        t0_score, t1_score = t1_score, t0_score
      res.append("*{}* (*{}* pts) vs. {} ({} pts)".format(t0, t0_score, t1, t1_score))
    return "\n\t".join(res)
