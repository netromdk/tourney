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
  "Thunderpants",
]

def simpleleet(s):
  return s.lower().\
    replace("a", "4").\
    replace("b", "8").\
    replace("e", "3").\
    replace("f", "ph").\
    replace("k", "x").\
    replace("l", "1").\
    replace("o", "0").\
    replace("s", "5").\
    replace("t", "7")

TEAM_NAME_DECORATIONS = [
  lambda x: "{} of Doom".format(x),
  lambda x: "{} +1".format(x),
  lambda x: "{} (Handicapped)".format(x),
  lambda x: "{} in the Membrane".format(x),
  lambda x: "{} on the Rocks".format(x),
  lambda x: "{} et al.".format(x),
  lambda x: "{} With Bells On".format(x),
  lambda x: "{}, Cherry on Top".format(x),
  lambda x: "{}! Here We Go Again".format(x),
  lambda x: "To {} Or Not To {}".format(x, x),
  lambda x: "Not {}".format(x),
  lambda x: "{}²".format(x),
  lambda x: "{} 2½".format(x),
  lambda x: "Blessed {}".format(x),
  lambda x: "Cursed {}".format(x),
  lambda x: "Punished {}".format(x),
  lambda x: "Shin {}".format(x),
  lambda x: "{} Stranding".format(x),
  lambda x: "{} 2: Son of {}".format(x, x),
  lambda x: "Bride of {}".format(x),
  lambda x: "Game of {}".format(x),
  lambda x: "Dawn of {}".format(x),
  lambda x: "Rise of {}".format(x),
  lambda x: "Battle for {}".format(x),
  lambda x: "Escape from {}".format(x),
  lambda x: "How to {} and Get Away With It".format(x),
  lambda x: "Operation {}".format(x),
  lambda x: "{} Begin Again".format(x),
  lambda x: "Look who's {} now!".format(x),
  lambda x: "{}: The Squeakquel".format(x),
  lambda x: "\"{}\"".format(x),
  lambda x: x.upper(),
  lambda x: x[::2],
  lambda x: x[::-1].lower().title(),
  lambda x: "I Can't Believe It's Not {}".format(x),
  lambda x: "".join([c if c.lower() not in "aeiouyæøå" else 'o' for c in x]),
  lambda x: "".join([choice([c.lower(), c.upper()]) for c in x]),  # nosec
  lambda x: simpleleet(x),
]

TEAM_NAME_PARTS = {
  "noun": [
    "Amigo",
    "Automaton",
    "Ark",
    "Bell",
    "Bride",
    "Clone",
    "Cobra",
    "Compiler",
    "Contingent",
    "Crusade",
    "Crystal",
    "Cyborg",
    "Daughter",
    "Disaster",
    "Dracula",
    "Dragon",
    "Drifter",
    "Drinker",
    "Dynamo",
    "Flamingo",
    "Football",
    "Frankenstein",
    "Game",
    "Godzilla",
    "Golem",
    "Groom",
    "Hurricane",
    "Hustler",
    "Interpreter",
    "Jedi",
    "Kicker",
    "Kingdom",
    "Lexer",
    "Loser",
    "Mafia",
    "Marionette",
    "Membrane",
    "Meme",
    "Menace",
    "Mullet",
    "Necromancer",
    "Operator",
    "Opossum",
    "Panda",
    "Parser",
    "Phenom",
    "Pint",
    "Piston",
    "Player",
    "Python",
    "Raider",
    "Ray Tracer",
    "Regiment",
    "Reserve",
    "Revenge",
    "Robot",
    "Rock",
    "Scorpion",
    "Seer",
    "Serpent",
    "Shoe",
    "Shooter",
    "Sith",
    "Skull",
    "Sorcerer",
    "Spider",
    "Spinner",
    "Squirrel",
    "Superstar",
    "Swashbuckler",
    "Temple",
    "Terminator",
    "Turtle",
    "Uniform",
    "Vader",
    "Vagabond",
    "Vagrant",
    "Viper",
    "Wanderer",
    "War",
    "Winner",
    "Wizard",
    "Wonder",
    ("Battalion", None),
    ("Brigade", None),
    ("Chaos", None),
    ("Cherry", "Cherries"),
    ("Club", None),
    ("Couch", "Couches"),
    ("Doom", None),
    ("Ducky", "Duckies"),
    ("Duo", None),
    ("Gang", None),
    ("Group", None),
    ("League", None),
    ("Legion", None),
    ("Platoon", None),
    ("Prodigy", "Prodigies"),
    ("Squad", None),
    ("Squadron", None),
    ("Team", None),
    ("Thunder", None),
    ("Trio", None),
    (None, "Pants"),
  ],
  "adjective": [
    "Amazing",
    "Anonymous",
    "Armchair",
    "Backwards",
    "Bad",
    "Barbed",
    "Bent",
    "Blessed",
    "Bloody",
    "Blunted",
    "Bona Fide",
    "Bonkers",
    "Brave",
    "Broken",
    "Centralized",
    "Chaotic",
    "Coalesced",
    "Coarse",
    "Congealed",
    "Contaminated",
    "Coordinated",
    "Courageous",
    "Crisscrossed",
    "Crystal",
    "Cursed",
    "Decentralized",
    "Deleted",
    "Dependable",
    "Designated",
    "Dodgy",
    "Draconian",
    "Drastic",
    "Dubious",
    "Dubitable",
    "Eccentric",
    "Eclectic",
    "Electric",
    "Erased",
    "Essential",
    "Evil",
    "Expunged",
    "Extraordinary",
    "Faceless",
    "Fantastic",
    "Fearless",
    "Flaming",
    "Gelled",
    "Glorious",
    "Good",
    "Gritty",
    "Heterogeneous",
    "Homogeneous",
    "Immoderate",
    "Incorporated",
    "Incredible",
    "Indefinable",
    "Indominable",
    "Injured",
    "Insane",
    "Inside-out",
    "Invalidated",
    "Jelled",
    "Lawful",
    "Last",
    "Lost",
    "Mad",
    "Meshed",
    "Nameless",
    "Neutral",
    "Nullified",
    "Obliterated",
    "Obscure",
    "Omitted",
    "Ordinary",
    "Overrated",
    "Phantom",
    "Plagued",
    "Poltroon",
    "Psychotic",
    "Punished",
    "Quashed",
    "Questionable",
    "Radical",
    "Raging",
    "Random",
    "Redacted",
    "Reliable",
    "Reprimanded",
    "Rescinded",
    "Reticulated",
    "Reversed",
    "Revolutionary",
    "Sideways",
    "Skilled",
    "Smart",
    "Solidified",
    "Super",
    "Tenacious",
    "Transposed",
    "Trustworthy",
    "Ultra",
    "Unbelievable",
    "Unbent",
    "Unbroken",
    "Uncultured",
    "Undead",
    "Undefined",
    "Underrated",
    "Undetermined",
    "Unhinged",
    "Unified",
    "Unmapped",
    "Unpredictable",
    "Unprocessed",
    "Unrefined",
    "Untraceable",
    "Unusual",
    "Upside-down",
    "Vague",
    "Vampire",
    "Veritable",
    "Zombie",
  ],
}

def nouns(n=1, p=False):
  nnouns = sample(TEAM_NAME_PARTS["noun"], n)  # nosec
  pnouns = []
  for noun in nnouns:
    pnoun = noun
    if type(noun) is tuple:
      if noun[0] is not None and noun[1] is None:
        # Some nouns do not have a plural form, and adding "s" is incorrect.
        pnoun = noun[0]
      elif p or noun[0] is None:
        # Some nouns should not be pluralized at all (for a teamname)
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
  lambda: "{} {}".format(noun(), noun(p=True)),  # Thunder Pants
  lambda: "{} {}".format(*nouns(n=2)),  # Monkey Python
  lambda: "{} {} {}".format(*(adjs(n=2) + nouns(p=True))),  # Tenacious Raging Bells
  lambda: "{} of the {} {}".format(noun(p=True), adj(), noun()),  # Raiders of the Lost Ark
]

def generate_teamnames(nteams):
  return [generate_teamname() for i in range(nteams)]

def generate_teamname():
  r = random()  # nosec
  if r < 0.1:
    return choice(TEAM_NAMES)  # nosec
  elif r < 0.9:
    return choice(TEAM_NAME_FORMS)()  # nosec
  else:
    return decorate_teamname(generate_teamname())

def decorate_teamname(name):
  return choice(TEAM_NAME_DECORATIONS)(name)  # nosec
