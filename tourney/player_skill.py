import json
import os
from trueskill import Rating, quality_1vs1, rate_1vs1, rate
from .constants import DATA_PATH
from .scores import Scores

class PlayerSkill:
  __instance = None

  def __init__(self):
    if not PlayerSkill.__instance:
      self.reset()

      try:
        self.load()
        if len(self.__player_skills) == 0:
          self.calc_player_skills()
      except Exception as ex:
        print("PlayerSkill file could not load: {}".format(self.file_path()))
        print(ex)

      PlayerSkill.__instance = self

  @staticmethod
  def get():
    if not PlayerSkill.__instance:
      return PlayerSkill()
    return PlayerSkill.__instance

  def file_path(self):
    return os.path.expanduser("{}/player_skill.json".format(DATA_PATH))

  def load(self):
    with open(self.file_path(), "r") as fp:
      data = json.load(fp)
      if "player_skills" in data:
        player_skills = data["player_skills"]
        for pskill in player_skills:
            self.__player_skills[pskill[0]] = Rating(pskill[1], pskill[2])

  def save(self):
    player_skills = [[p, ps.mu, ps.sigma] for p, ps in self.__player_skills.items()]
    data = {
      "player_skills": player_skills
    }
    os.makedirs(os.path.dirname(self.file_path()), exist_ok=True)
    with open(self.file_path(), "w+") as fp:
      json.dump(data, fp, indent=2)

  def reset(self):
    self.__player_skills = {}

  def get_player_skill(self, user_id):
    if user_id not in self.__player_skills:
      self.__player_skills[user_id] = Rating()
    return self.__player_skills[user_id]

  def get_team_skill(self, team):
    """ Average all mu values for the total team skill.
    Lower confidence a lot, since we're not sure about this at all.
    TODO: How much to lower the confidence?
    """
    team_skills = [self.get_player_skill(p) for p in team]
    avg_mu = sum(r.mu for r in team_skills) / len(team)
    # mu_dist = max([r.mu for r in team_skills]) - min([r.mu for r in team_skills])
    avg_sigma = sum(r.sigma ** 2 for r in team_skills) / len(team)
    team_skill = Rating(mu=avg_mu, sigma=avg_sigma)
    return team_skill

  def get_match_quality(self, match):
    if len(match) == 3:
      # Two teams in one match
      skill_a = self.get_team_skill(match[0])
      skill_b = self.get_team_skill(match[1])
      return quality_1vs1(skill_a, skill_b)
    elif len(match) == 4:
      # Three teams in three matches
      skill_a = self.get_team_skill(match[0])
      skill_b = self.get_team_skill(match[1])
      skill_c = self.get_team_skill(match[2])
      quality_ab = quality_1vs1(skill_a, skill_b)
      quality_ac = quality_1vs1(skill_a, skill_c)
      quality_bc = quality_1vs1(skill_b, skill_c)
      return min(quality_ab, quality_ac, quality_bc)

  def rate_uneven_match(self, win_team, lose_team):
    """Rates a match between differently-sized teams implementation,
    adjust each player as though they individually had won/lost
    against the average of the opposing team.
    TODO: Take into account that we might have really low confidence in the team.
    """
    win_team_skill = self.get_team_skill(win_team)
    lose_team_skill = self.get_team_skill(lose_team)
    new_win_team = []
    new_lose_team = []
    new_win_team_skill, new_lose_team_skill =\
        rate_1vs1(win_team_skill, lose_team_skill)

    for p in win_team:
      pskill = self.get_player_skill(p)
      new_skill, _ = rate_1vs1(pskill, lose_team_skill)
      self.__player_skills[p] = new_skill
      new_win_team.append(new_skill)
    for p in lose_team:
      pskill = self.get_player_skill(p)
      _, new_skill = rate_1vs1(win_team_skill, pskill)
      self.__player_skills[p] = new_skill
      new_lose_team.append(new_skill)

  def rate_even_match(self, win_team, lose_team):
    win_team_skills = [self.get_player_skill(p) for p in win_team]
    lose_team_skills = [self.get_player_skill(p) for p in lose_team]
    new_win_team_skills, new_lose_team_skills = rate([win_team_skills, lose_team_skills])
    for i in range(len(win_team)):
      win_p = win_team[i]
      lose_p = lose_team[i]
      new_win_p_skill = new_win_team_skills[i]
      new_lose_p_skill = new_lose_team_skills[i]
      self.__player_skills[win_p] = new_win_p_skill
      self.__player_skills[lose_p] = new_lose_p_skill

  def rate_match(self, win_team, lose_team):
    if len(win_team) == len(lose_team):
        return self.rate_even_match(win_team, lose_team)
    else:
        return self.rate_uneven_match(win_team, lose_team)

  def calc_player_skills(self):
    scores = Scores.get()
    for score in scores:
      if score[2] > score[4]:
        winteam = score[1]
        loseteam = score[3]
      else:
        winteam = score[3]
        loseteam = score[1]
      self.rate_match(winteam, loseteam)
    self.save()

  def test(self):
    self.__player_skills["TESTUSER1"] = Rating(15)
    self.__player_skills["TESTUSER2"] = Rating(50)
    self.__player_skills["TESTUSER3"] = Rating(25)
    self.__player_skills["TESTUSER4"] = Rating(35)
    self.__player_skills["TESTUSER6"] = Rating(45)
    team_a = ("TESTUSER1", "TESTUSER2", "TESTUSER6")
    team_b = ("TESTUSER3", "TESTUSER4")
    print("Teams: {} vs {}".format(team_a, team_b))
    quality = self.get_match_quality(team_a, team_b)
    print("Match quality: {}".format(quality))
    self.rate_match(team_a, team_b)
    quality = self.get_match_quality(team_a, team_b)
    print(self.get_player_skill("TESTUSER1"))
    print(quality)
