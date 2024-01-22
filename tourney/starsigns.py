import os
import json
from random import choice, random

from .constants import DATA_PATH

western_zodiac = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
other = 'Unknown'

chinese_zodiac = ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig']
chinese_comp = {sign : {other : "average" for other in [x for x in chinese_zodiac if x != sign]} for sign in chinese_zodiac}
better_indices = [1, -1, 9, 7, 5, 3, 1, -1, -3, -5, -7, -9]
worst_indices = [7, 5, 3, 1, -1, -3, -5, -7, 3, 1, -1, -3]
for i in range(len(chinese_zodiac)):
    # "best" compatibility
    chinese_comp[chinese_zodiac[i]][chinese_zodiac[(i+4)%12]] = "best"
    chinese_comp[chinese_zodiac[i]][chinese_zodiac[(i+8)%12]] = "best"
    # "better" compatibility
    chinese_comp[chinese_zodiac[i]][chinese_zodiac[i+better_indices[i]]] = "better"
    # "worse" compatibility
    chinese_comp[chinese_zodiac[i]][chinese_zodiac[(i+6)%12]] = "worse"
    # "worst" compatibility
    chinese_comp[chinese_zodiac[i]][chinese_zodiac[i+worst_indices[i]]] = "worst"
for s in chinese_zodiac:
    best = [s2 for s2 in chinese_comp[s].keys() if chinese_comp[s][s2] == "best"]
    better = [s2 for s2 in chinese_comp[s].keys() if chinese_comp[s][s2] == "better"]
    average = [s2 for s2 in chinese_comp[s].keys() if chinese_comp[s][s2] == "average"]
    worse = [s2 for s2 in chinese_comp[s].keys() if chinese_comp[s][s2] == "worse"]
    worst = [s2 for s2 in chinese_comp[s].keys() if chinese_comp[s][s2] == "worst"]
    print(best, better, average, worse, worst)

def compatibility(sign1, sign2):
  if sign1 == unknown_zodiac and sign2 == unknown_zodiac:
    # Strange signs are compatible
    return 0.9  # nosec
  if sign1 in western_zodiac and sign2 in western_zodiac:
    # Use source ... for western comparisons
    return 1
  if sign1 in chinese_zodiac and sign2 in chinese_zodiac:
    return 1
  elif (sign1 in chinese_zodiac and sign2 in western_zodiac) or (sign1 in western_zodiac and sign2 in chinese_zodiac):
  # East/West mix
    if sign1 in chinese_zodiac:
      east = sign1
      west = sign2
    else:
      east = sign2
      west = sign1
    return 0.5
  else:
    # Strange signs are incompatible with normal ones
    return 0.1

def guess_sign():
  r = random()
  if r < 0.45:
    sign = choice(western_zodiac)
  elif r < 0.90:
    sign = choice(chinese_zodiac)
  else:
    sign = 'unknown'
  return sign
  
def guess_str(sign):
  if sign in western_zodiac:
    def article(sign_name):
      if sign_name[0] in 'aieouy':
        return "an " + sign_name
      else:
        return "a " + sign_name
      
    west_guesses = [
      "{}, if I'm not mistaken.",
      "I bet you're {}.",
      "I think you're {}.",
      "If you're not {} then I am sorely mistaken. And I seldom am.",
      "Joining like that, you must be {}.",
      "My senses tell me you're {}.",
      "Well you're obviously {}.",
      "You have to be {}.",
      "You seem like {}.",
      "You strike me as {}.",
      "You're {}, aren't you?",
    ]
    
    return choice(guesses).format(article(sign).title())  # nosec
  elif sign in chinese_zodiac:
    east_guesses = [
      "You were born in{}, if I'm not mistaken.",
      "I bet you were born in {}.",
      "I think you were born in {}.",
      "Joining like that, you must have been born in{}.",
      "My senses tell me you were born in {}.",
      "Well you were obviously born in {}.",
      "You must have been born in {}.",
      "You seem like you were born in {}.",
      "You strike me as someone who was born in {}.",
      "You were born in {}, weren't you?",
    ]
    
    return choice(east_guesses).format("the year of the {}".format(sign.title()))  # nosec
  else:
    unknown_guesses = [
      "Were you born on a distant planet?",
      "Were you born underground?",
      "Were you grown in a vat?",
      "Are you a clone?",
      "Have you absorbed any twins?",
      "Are you from a parallel universe?",
      "Are you from an alternate timeline?",
      "Are you a djinn, spirit or ghost?",
      "Have you sold it?",
      "Did you lose it?",
      "Are you astrally projecting here?",
      "Were you cursed?",
      "Were you born a REALLY long time ago?",
      "Have you ever walked through a mirrors?",
      "That must suck."
    ]
    return "You don't seem to have a normal starsign. " + \
      choice(unknown_guesses) + " Terrestrial astrology may not apply to you."  # nosec

class Starsigns:
  __instance = None

  def __init__(self):
    if not Starsigns.__instance:
      self.reset()
      try:
        self.load()
      except Exception as ex:
        print("Starsign file could not load: {}".format(self.file_path()))
        print(ex)

      Starsigns.__instance = self

  @staticmethod
  def get():
    if not Starsigns.__instance:
      return Starsigns()
    return Starsigns.__instance

  def add(self, user_id, starsign):
    """Add a starsign for a given player."""
    # Remove old starsign
    self.remove(user_id)
    # Add the new one
    self.__starsigns.append([user_id, starsign])

  def guess_sign(self, user_id):
    # Intuit a sign for the user
    sign = guess_sign()
    self.add(user_id, sign)
    return guess_str(sign)

  def remove(self, user_id):
    self.__starsigns = [x for x in self.__starsigns if set(x[0]) != user_id]

  def starsign(self, user_id):
    if self.__starsigns:
      return self.__starsigns[user_id]
    return None

  def file_path(self):
    return os.path.expanduser("{}/starsigns.json".format(DATA_PATH))

  def reset(self):
    self.__starsigns = []

  def save(self):
    data = {
      "starsigns": self.__starsigns,
    }
    os.makedirs(os.path.dirname(self.file_path()), exist_ok=True)
    with open(self.file_path(), "w+", encoding="utf-8") as fp:
      json.dump(data, fp)

  def load(self):
    with open(self.file_path(), "r", encoding="utf-8") as fp:
      data = json.load(fp)
      if "starsigns" in data:
        self.__starsigns = data["starsigns"]
