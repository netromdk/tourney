from random import sample, choice, random

TEAM_NAMES = [
  "Air Farce",
  "Cereal Killers",
  "Dangerous Dynamos",
  "Designated Drinkers",
  "Fantastic Four",
  "Fire Breaking Rubber Duckies",
  "Game of Throw-ins",
  "Glorious Bastards",
  "Injured Reserve",
  "Monkey Python",
  "One Hit Wonders",
  "Our Uniforms Match",
  "Pique Blinders",
  "Pistons from the Past",
  "Purple Cobras",
  "Rabid Squirrels",
  "Raging Nightmare",
  "Recipe for Disaster",
  "Shockwave",
  "Smarty Pints",
  "Straight off the Couch",
  "Tenacious Turtles",
  "The Abusement Park",
  "The Flaming Flamingos",
  "The League of Ordinary Gentlemen",
  "The Meme Team",
  "The Mullet Mafia",
  "Thunderpants"
]

TEAM_NAME_DECORATIONS = [
  lambda x: "{} of Doom".format(x),
  lambda x: "{} +1".format(x),
  lambda x: "{} (Handicapped)".format(x),
  lambda x: "{} in the Membrane".format(x),
  lambda x: "{} on the Rocks".format(x),
  lambda x: "{} et al.".format(x),
  lambda x: "{} With Bells On".format(x),
  lambda x: "{}, Cherry on Top".format(x),
  lambda x: "Not {}".format(x),
  lambda x: "{}²".format(x),
  lambda x: "Blessed {}".format(x),
  lambda x: "Cursed {}".format(x),
  lambda x: "Punished {}".format(x),
  lambda x: "Shin {}".format(x),
  lambda x: "{} Stranding".format(x),
  lambda x: "{} 2: Son of {}".format(x, x),
  lambda x: "Bride of {}".format(x),
  lambda x: "Game of {}".format(x),
  lambda x: "\"{}\"".format(x),
  lambda x: x.upper(),
  lambda x: x[::2],
  lambda x: x[::-1].lower().title(),
  lambda x: "I Can't Believe It's Not {}".format(x),
  lambda x: "".join([c if c.lower() not in "aeiouyæøå" else 'o' for c in x]),
]

TEAM_NAME_PARTS = {
  "noun": [
    "Amigo",
    "Bell",
    "Bride",
    "Chaos",
    "Club",
    "Cobra",
    "Compiler",
    "Daughter",
    "Disaster",
    "Doom",
    "Dracula",
    "Dragon",
    "Drinker",
    "Duo",
    "Dynamo",
    "Flamingo",
    "Football",
    "Frankenstein",
    "Game",
    "Gang",
    "Godzilla",
    "Groom",
    "Group",
    "Hurricane",
    "Kicker",
    "League",
    "Legion",
    "Loser",
    "Mafia",
    "Membrane",
    "Meme",
    "Mullet",
    "Pint",
    "Piston",
    "Player",
    "Python",
    "Ray Tracer",
    "Reserve",
    "Rock",
    "Shoe",
    "Shooter",
    "Spider",
    "Spinner",
    "Squirrel",
    "Team",
    "Thunder",
    "Trio",
    "Turtle",
    "Uniform",
    "Winner",
    "Wonder",
    ("Cherry", "Cherries"),
    ("Couch", "Couches"),
    ("Ducky", "Duckies"),
    (None, "Pants"),
  ],
  "adjective": [
    "Amazing",
    "Bad",
    "Blessed",
    "Bloody",
    "Chaotic",
    "Cursed",
    "Dependable",
    "Designated",
    "Eccentric",
    "Eclectic",
    "Electric",
    "Evil",
    "Extraordinary",
    "Fantastic",
    "Flaming",
    "Glorious",
    "Good",
    "Indominable",
    "Injured",
    "Insane",
    "Lawful",
    "Neutral",
    "Ordinary",
    "Overrated",
    "Punished",
    "Raging",
    "Random",
    "Sideways",
    "Skilled",
    "Smart",
    "Super",
    "Tenacious",
    "Undead",
    "Underrated",
    "Unpredictable",
    "Upside-down",
    "Vampire",
    "Zombie",
  ],
}

def nouns(n=1, p=False):
  nnouns = sample(TEAM_NAME_PARTS["noun"], n)  # nosec
  pnouns = []
  for noun in nnouns:
    pnoun = noun
    if type(noun) is tuple:
      if p or noun[0] is None:
        pnoun = noun[1]
      else:
        pnoun = noun[0]
    elif p:
      pnoun = "{}s".format(noun)
    pnouns.append(pnoun)
  return pnouns

def noun(p=False):
  return nouns(n=1, p=p)[0]

def adjs(n=1):
  return sample(TEAM_NAME_PARTS["adjective"], n)  # nosec

def adj():
  return adjs(n=1)[0]

TEAM_NAME_FORMS = [
  lambda: "The {} {}".format(adj(), noun(p=True)),  # The Flaming Flamingos
  lambda: "{}{}".format(noun(), noun(p=True).lower()),  # Thunderpants
  lambda: "{} {}".format(*nouns(n=2)),  # Monkey Python
  lambda: "{} {} {}".format(*(adjs(n=2) + nouns()))  # Tenacious Raging Bells
]

def generate_teamnames(nteams):
  teamnames = [generate_teamname() for i in range(nteams)]
  return teamnames

def generate_teamname():
  r = random()  # nosec
  if r < 0.1:
    return choice(TEAM_NAMES)   # nosec
  elif r < 0.9:
    return choice(TEAM_NAME_FORMS)()   # nosec
  else:
    return decorate_teamname(generate_teamname())

def decorate_teamname(name):
  return choice(TEAM_NAME_DECORATIONS)(name)   # nosec
