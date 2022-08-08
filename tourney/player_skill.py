import json
import os
from trueskill import Rating, quality, rate, quality_1vs1, rate_1vs1
from .constants import DATA_PATH
from .scores import Scores

class PlayerSkill:
  __instance = None

  def __init__(self):
    if not PlayerSkill.__instance:
      self.reset()

      try:
        self.load()
      except Exception as ex:
        print("PlayerSkill file could not load: {}".format(self.file_path()))
        print(ex)

      if len(self.__player_skills) == 0:
        self.calc_player_skills()

      PlayerSkill.__instance = self

  @staticmethod
  def get():
    if not PlayerSkill.__instance:
      return PlayerSkill()
    return PlayerSkill.__instance

  def file_path(self):
    return os.path.expanduser("{}/player_skill.json".format(DATA_PATH))

  def load(self):
    with open(self.file_path(), "r", encoding="utf-8") as fp:
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
    with open(self.file_path(), "w+", encoding="utf-8") as fp:
      json.dump(data, fp, indent=2)

  def reset(self):
    self.__player_skills = {}

  def get_player_skill(self, user_id):
    if user_id not in self.__player_skills:
      self.__player_skills[user_id] = Rating()
    return self.__player_skills[user_id]

  def __convervative_rank(self, rating):
    """Microsoft's approach: Player ranks are displayed as the conservative estimate of their skill,
    R = μ − 3 × σ. This is conservative, because the system is 99% sure that the player's skill is
    actually higher than what is displayed as their rank.
    """
    return rating.mu - 3 * rating.sigma

  def get_player_rank(self, user_id):
    return self.__convervative_rank(self.get_player_skill(user_id))

  def get_player_placement(self, user_id):
    """The conservative rank placement of user among all other players.
    """
    rankings = []
    for other_user_id in self.__player_skills:
      rank = self.__convervative_rank(self.__player_skills[other_user_id])
      rankings.append((other_user_id, rank))

    # Sort highest rankings at the top.
    rankings.sort(key=lambda x: x[1], reverse=True)

    placement = 0
    for (user, rank) in rankings:
      placement += 1
      if user == user_id:
        return placement
    return placement

  def get_team_skill(self, team):
    """ Average all mu values for the total team skill.
    Lower confidence a lot, since we're not sure about this at all.
    TODO: How much to lower the confidence?
    """
    team_skills = [self.get_player_skill(p) for p in team]
    avg_mu = sum(r.mu for r in team_skills) / len(team)
    # mu_dist = max([r.mu for r in team_skills]) - min([r.mu for r in team_skills])
    avg_sigma = sum(r.sigma for r in team_skills) / len(team)
    avg_sigma = avg_sigma * 2  # Increase uncertainty in averaged team skills
    team_skill = Rating(mu=avg_mu, sigma=avg_sigma)
    return team_skill

  def __modify_team_sigmas_by_mu_ratio(self, team_skills):
    """Modify team sigmas by mu ratio such that the difference in skill is taken into consideration.
    A strong player and a less strong player won't likely be matched up against two strong players
    when this is done. And it means players won't always play the same group of persons, too.
    """
    mus = [r.mu for r in team_skills]
    mu_diff = mus[0]
    for mu in mus[1:]:
      mu_diff -= mu
    mu_diff = abs(mu_diff)
    mu_ratio = (1.0 / (mu_diff / max(mus)))
    res_skills = []
    for p in team_skills:
      res_skills.append(Rating(mu=p.mu, sigma=p.sigma + p.sigma * (mu_ratio / max(mus))))
    return res_skills

  def get_match_quality(self, match):
    team_a, team_b = match[0], match[1]
    # Two teams in one match, number of rounds ignored
    if len(match[0]) == len(match[1]):
      team_a_skills = [self.get_player_skill(p) for p in team_a]
      team_a_skills = self.__modify_team_sigmas_by_mu_ratio(team_a_skills)
      team_b_skills = [self.get_player_skill(p) for p in team_b]
      team_b_skills = self.__modify_team_sigmas_by_mu_ratio(team_b_skills)
      return quality([team_a_skills, team_b_skills])
    else:
      # Unmatched teams, aggregate team skill and rate as 1vs1
      skill_team_a = self.get_team_skill(team_a)
      skill_team_b = self.get_team_skill(team_b)
      return quality_1vs1(skill_team_a, skill_team_b)

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
    try:
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
    except FloatingPointError:
      print("Skill difference too high: {} vs {}. Ratings not updated".
            format(win_team_skill, lose_team_skill))

  def rate_even_match(self, win_team, lose_team):
    win_team_skills = [self.get_player_skill(p) for p in win_team]
    lose_team_skills = [self.get_player_skill(p) for p in lose_team]
    try:
      new_win_team_skills, new_lose_team_skills = rate([win_team_skills, lose_team_skills])
      for i in range(len(win_team)):
        win_p = win_team[i]
        lose_p = lose_team[i]
        new_win_p_skill = new_win_team_skills[i]
        new_lose_p_skill = new_lose_team_skills[i]
        self.__player_skills[win_p] = new_win_p_skill
        self.__player_skills[lose_p] = new_lose_p_skill
    except FloatingPointError:
      print("Skill difference too high: {} vs {}. Ratings not updated".
            format(win_team_skills, lose_team_skills))

  def rate_match(self, win_team, lose_team):
    if len(win_team) == len(lose_team):
        return self.rate_even_match(win_team, lose_team)
    else:
        return self.rate_uneven_match(win_team, lose_team)

  def calc_player_skills(self):
    scores = Scores.get()
    for score in scores.matches():
      if score[2] > score[4]:
        winteam = score[1]
        loseteam = score[3]
      else:
        winteam = score[3]
        loseteam = score[1]
      self.rate_match(winteam, loseteam)
    self.save()

  def test(self):
    old_skills = self.__player_skills
    self.__player_skills = {}
    self.__player_skills["TESTUSER1"] = Rating(15)
    self.__player_skills["TESTUSER2"] = Rating(25)
    self.__player_skills["TESTUSER3"] = Rating(35)
    self.__player_skills["TESTUSER4"] = Rating(25)
    self.__player_skills["TESTUSER5"] = Rating(25)
    self.__player_skills["TESTUSER6"] = Rating(25)
    team_a = ("TESTUSER1", "TESTUSER2", "TESTUSER3")
    team_b = ("TESTUSER4", "TESTUSER5")
    team_c = ("TESTUSER6")

    mquality = self.get_match_quality((team_a, team_a, 2))
    print("Mirror match quality: {}".format(mquality))

    mquality = self.get_match_quality((team_a, team_b, 2))
    print("3v2 even? match quality: {}".format(mquality))
    self.rate_match(team_a, team_b)
    mquality = self.get_match_quality((team_a, team_b, 2))
    print("3v2 match quality after unlikely win: {}".format(mquality))
    mquality = self.get_match_quality((team_a, team_c, 2))
    print("2v1 even? match quality: {}".format(mquality))
    self.rate_match(team_a, team_c)
    print("2v1 match quality after win: {}".format(mquality))

    mquality = self.get_match_quality((team_a, team_a, 2))
    print("Mirror match quality: {}".format(mquality))

    self.__player_skills = old_skills
