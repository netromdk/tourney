import os
import json
from random import choice, random

from .constants import DATA_PATH

western_zodiac = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
chinese_zodiac = ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig']
other = 'Unknown'

class Starsign:
    def __init__(self, name):
        self.__name = "Unknown"

    def compatibility(self, other):
        if type(self) is UnknownStarsign and type(other) is UnknownStarsign:
            # Others are compatible
            return 0.9  # nosec
        if type(self) is WesternStarsign and type(other) is WesterstarSign:
            # Use source ... for western comparisons
            return 1
        else if type(self) is ChineseStarsign and type(other) is ChineseStarsign:
            # Use source https://www.lovetoknow.com/life/astrology/chinese-zodiac-marriage-combinations for chinese comparisons
            matrix ="""\
                                Traits                                                  Ideal                                      Good                           Difficult                              Worst
                   RAT          No long-lasting friendships, determined, ambitious      Rat, Ox, Pig                               Dragon, Monkey, Tiger          Snake, Ram, Rooster                    Rabbit, Horse, Dog
                   OX           Loner, inspiration to others, wonderful parent          Monkey, Snake, Rat                         Ox, Rooster, Rabbit            Dragon, Ram, Dog, Pig                  Tiger, Horse
                   TIGER        Brave, aggressive yet caring                            Horse, Dog, Pig                            Rat                            Tiger, Dragon, Snake, Rooster          Rabbit, Ram, Monkey, Ox
                   RABBIT       Lucky and rather shy by affectionate                    Dragon, Pig, Ram                           Rabbit, Snake, Ox, Dog, Monkey Horse, Rooster                         Rat, Tiger
                   DRAGON       Robust and passionate about life                        Snake, Ram, Monkey, Rabbit                 Pig, Rooster, Rat              Horse, Dog, Ox, Tiger                  Dragon
                   SNAKE        Hard-worker, friendly, calm                             Rooster, Dragon, Ox                        Rabbit                         Snake, Tiger, Horse, Ram, Monkey, Rat  Dog, Pig
                   HORSE        Goal-oriented, See all sides, sense of humor            Ram, Dog, Tiger                            Dragon                         Horse, Rooster, Pig, Rabbit, Snake     Monkey, Rat, Ox
                   RAM          Homebody, social, artistic                              Rabbit, Pig, Dragon, Horse                 Monkey                         Ram, Rat, Ox, Snake                    Rooster, Dog, Tiger
                   MONKEY       Curious, playful, prankster                             Dragon, Ox                                 Monkey, Rat, Rabbit, Ram       Rooster, Dog, Pig, Snake               Tiger, Horse
                   ROOSTER      Multi-Taskers, ambitious, expectant                     Pig, Snake                                 Ox, Dragon                     Dog, Rat, Tiger, Rabbit, Horse, Monkey Rooster, Ram
                   DOG          Loyal, honest, leader                                   Pig, Tiger Horse                           Rabbit                         Dog, Ox, Dragon, Monkey, Rooster       Rat, Snake, Ram
                   PIG          Planner, leader, family-oriented                        Pig, Rat, Ram, Rabbit, Tiger, Rooster, Dog Dragon                         Ox, Horse, Monkey                      Snake """
            return 1
        else if type(self) is ChineseStarsign and type(other) is WesternStarsign or type(self) is WesternStarsign and type(other) is ChineseStarsign:
            # East/West mix
            if type(self) is ChineseStarsign:
                east = self
                west = other
                return 0.5
            else:
                east = other
                west = self
                return 0.5
            return 0.5
        else:
            # Unknown mixes are incompatible
            return random(0.5)  # nosec
        
        if isinstance(other, WesterStarsign)

    def sign(self):
        return self.__name
    
class WesternStarsign(Starsign):
    def __init__(self):
        super.__init__()

    def guess_str():
        if self.__name not in western_zodiac:
            return "I'm not sure what sign you are!"

        guesses = [
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
        def article(sign_name):
            if sign_name[0] in 'aieouy':
                return "An " + sign_name
            else:
                return "A " + sign_name
        return choice(guesses).format(article(self.__name))  # nosec

    def guess():
        self.__name = choice(western_zodiac)  # nosec

class ChineseStarsign(Starsign):
    def __init__(self):
        super.__init__()

    def guess_str():
        if self.__name not in chinese_zodiac:
            return "I'm not sure what year you were born in!"
        
        guesses = [
            "You were born in the year of the {}, if I'm not mistaken.",
            "I bet you were born in the year of the {}.",
            "I think you were bornin the year of the {}.",
            "Joining like that, you must have been born in the year of the {}.",
            "My senses tell me you were born in the year of the {}.",
            "Well you were obviously born in the year of the {}.",
            "You must have been born in the year of the {}.",
            "You seem like you were born in the year of the {}.",
            "You strike me as someone who was born in the year of the {}.",
            "You were born in the year of the {}, weren't you?",
            ]
        return choice(guesses).format(self.__name)  # nosec

    def guess():
        self.__name = choice(chinese_zodiac)  # nosec
    def guess():


    def sign():
        return("Unknown")

class UnknownStarsign(Starsign):
    def __init__(self):
        super.__init__()

    def guess_str():
        guesses = [
            "Were you born on a distant planet?",
            "Were you born underground?",
            "Were you grown in a vat?",
            "Are you a clone?",
            "Have you absorbed any twins?",
            "Are you from a parallel universe?",
            "Are you a djinn, spirit or ghost?",
            "Have you sold it?",
            "Are you astrally projecting here?",
            "Were you cursed?",
            "Were you born a REALLY long time ago?",
            ]
        return "You don't seem to have a normal starsign. " + \
            choice(guesses) + " Terrestrial astrology may not apply to you."# nosec
        
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
    

  def remove(self, user_id):
    self.__starsigns = [x for x in self.__starsigns if set(x[0]) != user_id]

  def starsign(self, user_id):
    if starsigns:
      return starsigns[user_id]
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
