from random import sample, choice, random, choices, shuffle
from .constants import SEASON, SEASONS

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
  "Pin Droppers",
  "Pique Blinders",
  "Pistons from the Past",
  "Purple Cobras",
  "Rabid Squirrels",
  "Raging Nightmare",
  "Recipe for Disaster",
  "Shockwave",
  "Silent but Deadly",
  "Silent Night, Holy Night",
  "Smarty Pints",
  "Straight off the Couch",
  "Tenacious Turtles",
  "The Abusement Park",
  "The Flaming Flamingos",
  "The League of Ordinary Gentlemen",
  "The Meme Team",
  "The Mullet Mafia",
  "Thunderpants",
  "Western Front",
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
  lambda x: f"{x} of Doom",
  lambda x: f"{x} +1",
  lambda x: f"{x} (Handicapped)",
  lambda x: f"{x} in the Membrane",
  lambda x: f"{x} on the Rocks",
  lambda x: f"{x} et al.",
  lambda x: f"{x} With Bells On",
  lambda x: f"{x}, Cherry on Top",
  lambda x: f"{x}! Here We Go Again",
  lambda x: f"To {x} Or Not To {x}",
  lambda x: f"Not {x}",
  lambda x: f"{x}²",
  lambda x: f"{x} 2½",
  lambda x: f"Blessed {x}",
  lambda x: f"Cursed {x}",
  lambda x: f"Punished {x}",
  lambda x: f"Shin {x}",
  lambda x: f"{x} Stranding",
  lambda x: f"{x} 2: Son of {x}",
  lambda x: f"Bride of {x}",
  lambda x: f"Game of {x}",
  lambda x: f"Dawn of {x}",
  lambda x: f"Rise of {x}",
  lambda x: f"Battle for {x}",
  lambda x: f"Escape from {x}",
  lambda x: f"How to {x} and Get Away With It",
  lambda x: f"Operation {x}",
  lambda x: f"{x} Begin Again",
  lambda x: f"Look who's {x} now!",
  lambda x: f"{x}: The Squeakquel",
  lambda x: f"\"{x}\"",
  lambda x: x.upper(),
  lambda x: " ".join([w[::2] for w in x.split(" ")]),
  lambda x: x[::-1].lower().title(),
  lambda x: f"I Can't Believe It's Not {x}",
  lambda x: "".join([c if c.lower() not in "aeiouyæøå" else 'o' for c in x]),
  lambda x: "".join([choice([c.lower(), c.upper()]) for c in x]),  # nosec
  lambda x: simpleleet(x),
]

TEAM_NAME_PARTS = {
  None: {
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
      "Earmuff",
      "Flamingo",
      "Football",
      "Frankenstein",
      "Game",
      "Godzilla",
      "Golem",
      "Grave",
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
      "Silence",
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
      "Whisper",
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
      ("Hush", "Hushes"),
      ("League", None),
      ("Legion", None),
      ("Mouse", "Mice"),
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
      "Careful",
      "Careless",
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
      "Inaudible",
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
      "Mute",
      "Muted",
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
      "Quiet",
      "Radical",
      "Raging",
      "Random",
      "Redacted",
      "Reliable",
      "Reprimanded",
      "Rescinded",
      "Reserved",
      "Reticulated",
      "Reversed",
      "Revolutionary",
      "Sideways",
      "Silent",
      "Skilled",
      "Smart",
      "Sneaking",
      "Sneaky",
      "Solidified",
      "Soundless",
      "Stealthy",
      "Still",
      "Super",
      "Stealthy",
      "Tenacious",
      "Transposed",
      "Tranquil",
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
  },
  "easter": {
    "noun": [
      'Angel',
      'Apostle',
      'Centurion',
      'Chocolate',
      'Christ',
      'Crown',
      'Beer',
      'Disciple',
      'Donkey',
      'Egg',
      'Feast',
      'Full Moon',
      'Friday',
      'Hare',
      'Iscariot',
      'Kangaroo',
      'Lamb',
      'Nail',
      'Palm',
      'Passion',
      'Pedicure',
      'Plague',
      'Psalm',
      'Rabbit',
      'Savior',
      'Sermon',
      'Spear',
      'Sponge',
      'Sunday',
      'Supper',
      'Surprise',
      'Thorn',
      'Thursday',
      'Zombie',
      ('Bunny', 'Bunnies'),
      ('Candy', 'Candies'),
      ('Cross', 'Crosses'),
      ('Crucifix', 'Crucifixes'),
      ('Destiny', None),
      ('Foot', 'Feet'),
      ('Gækkebrev', 'Gækkebreve'),
      ('Jesus', 'Jesi'),
      ('Judas', 'Judases'),
      ('Lance', 'Lances'),
      ('Lily', 'Lilies'),
      ('Longinus', 'Longinuses'),
      ('Lunch', 'Lunches'),
      ('Mass', 'Masses'),
      (None, 'Pieces of Silver'),
      ('Redeemer', None),
      ('Snaps', 'Snapse')
    ],
    "adjective": [
      'Arch',
      'Bloody',
      'Candy',
      'Chocolate',
      'Clean',
      'Crucified',
      'Dead',
      'Easter',
      'Fasting',
      'Good',
      'Last',
      'Long',
      'Lunar',
      'Maundy',
      'Nailed',
      'Penultimate',
      'Pesach',
      'Re-animated',
      'Resurrected',
      'Risen',
      'Saved',
      'Spring',
      'Suffering',
      'Thirty',
      'Thorned',
      'Tortured',
      'Undead',
      'Vinegar',
      'Zombie',
    ]
  },
  "xmas": {
    "noun": [
      'Angel',
      'Bell',
      'Blizzard',
      'Cane',
      'Card',
      'Carol',
      'Caroler',
      'Chestnut',
      'Chocolate',
      'Christ',
      'Clause',
      'Coal',
      'Cookie',
      'Decoration',
      'Eve',
      'Father',
      'Fireplace',
      'Gift',
      'Holiday',
      'King',
      'Manger',
      'Night',
      'Nutcracker',
      'Ornament',
      'Present',
      'Santa',
      'Scrooge',
      'Sled',
      'Sleigh',
      'Snow',
      'Snowball',
      'Snowflake',
      'Stocking',
      'Sweater',
      'Tree',
      'Turkey',
      'Winter',
      ("Krampus", "Krampi"),
      ("Candy", "Candies"),
      (None, "Claws"),
      ('Christmas', 'Christmasses'),
      ('Cinnamon', None),
      ("Elf", "Elves"),
      (None, 'Holly'),
      ("Navidad", "Navidadez"),
      ('Reindeer', 'Reindeer'),
      ("Snowman", "Snowmen"),
      (None, 'Tidings'),
    ],
    "adjective": [
      'Candy',
      'Chilly',
      'Christmas',
      'Commercialized',
      'Feliz',
      'Festive',
      'Frosty',
      'Gingerbread',
      'Holy',
      'Jingle',
      'Jolly',
      'Merry',
      'Naughty',
      'Nice',
      'Pumpkin Spice',
      'Seasonal',
      'Winter',
      'Xmas',
      'Yule',
      'Yuletide',
      'Zombie']
  }
}

def parts_for_season(season=None):
  if season in TEAM_NAME_PARTS:
    return TEAM_NAME_PARTS[season]
  return TEAM_NAME_PARTS[None]

def n_parts_by_season(n=1):
  # Decide how many parts to sample from each season
  nparts_by_season = {}
  if SEASON is None:
    p_none = 1 - sum(SEASONS.values())
    # Split SEASONS into lists
    seasons, probs = map(list, zip(*SEASONS.items()))
    seasons.append(None)
    probs.append(p_none)
    part_seasons = choices(seasons, weights=probs, k=n)  # nosec
    print(part_seasons)
    nparts_by_season = {s: part_seasons.count(s) for s in set(part_seasons)}
  else:
    nparts_by_season[SEASON] = n

  return nparts_by_season

def get_parts(n_by_s, ptype):
  # Sample the nouns from the part list
  parts = []
  for s, sn in n_by_s.items():
    season_parts = parts_for_season(s)[ptype]
    parts += sample(season_parts, sn)  # nosec

  return parts

def nouns(n=1, p=False):
  nnouns_by_season = n_parts_by_season(n)

  # Sample the nouns from the part list
  noun_parts = get_parts(nnouns_by_season, "noun")

  # Pluralise the selected noun parts
  plur_nouns = []
  for noun_part in noun_parts:
    plur_noun = noun_part
    if isinstance(noun_part, tuple):
      if noun_part[0] is not None and noun_part[1] is None:
        # Some nouns do not have a plural form, and adding "s" is incorrect.
        plur_noun = noun_part[0]
      elif p or noun_part[0] is None:
        # Some nouns should not be pluralized at all (for a teamname)
        plur_noun = noun_part[1]
      else:
        plur_noun = noun_part[0]
    elif p:
      plur_noun = "{}s".format(noun_part)
    plur_nouns.append(plur_noun)

  # Shuffle the resulting list and return
  shuffle(plur_nouns)  # nosec
  return plur_nouns

def noun(p=False):
  return nouns(n=1, p=p)[0]

def adjs(n=1):
  nadjs_by_season = n_parts_by_season(n)

  # Sample the nouns from the part list
  adjs = get_parts(nadjs_by_season, "adjective")

  return adjs

def adj():
  return adjs(n=1)[0]

TEAM_NAME_FORMS = [
  lambda: "The {} {}".format(adj(), noun(p=True)),  # The Flaming Flamingos
  lambda: "{}{}".format(noun(), noun(p=True).lower()),  # Thunderpants
  lambda: "{} {}".format(noun(), noun(p=True)),  # Thunder Pants
  lambda: "{} {}".format(*nouns(n=2)),  # Monkey Python
  lambda: "{} {} {}".format(*(adjs(n=2) + nouns(p=True))),  # Tenacious Raging Bells
  lambda: "{} of the {} {}".format(noun(p=True), adj(), noun()),  # Raiders of the Lost Ark
  lambda: "The {} of {}".format(noun(), noun(p=True)),  # The Ace of Spades
  lambda: "The {} of the {}".format(*nouns(n=2)),  # The Passion of the Christ
  lambda: "{} {}".format(adj(), noun(p=True)),  # Tenacious Turtles
]

def generate_teamnames(nteams):
  return [generate_teamname() for i in range(nteams)]

def generate_teamname():
  teamname = ""
  r = random()  # nosec
  if r < 0.1 and SEASON is None:
    # Only use pre-defined teamnames outside of special seasons, p=0.1
    teamname = choice(TEAM_NAMES)  # nosec
  elif r < 0.9:
    teamname = choice(TEAM_NAME_FORMS)()  # nosec
  else:
    teamname = decorate_teamname(generate_teamname())
  return teamname

def decorate_teamname(name):
  return choice(TEAM_NAME_DECORATIONS)(name)  # nosec
