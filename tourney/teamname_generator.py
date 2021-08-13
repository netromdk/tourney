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
    "noun" : [
        "Ray Tracer",
        "Compiler",
        "Shooter",
        "Spinner",
        "Kicker",
        "Flamingo",
        "Team",
        "Gang",
        "Club",
        "Mafia",
        "Pint",
        "Player",
        "Game",
        "Group",
        "Trio",
        "Duo",
        "Legion",
        "Amigo",
        "Hurricane",
        "Chaos",
        "Disaster",
        "Cobra",
        "Squirrel",
        "Python",
        "Wonder",
        "Uniform",
        "Piston",
        "Dynamo",
        "Drinker",
        "Turtle",
        "Mullet",
        "Reserve",
        (None, "Pants"),
        "Meme",
        "Membrane",
        "Rock",
        "Doom",
        "Bell",
        ("Cherry", "Cherries"),
        "League",
        ("Couch", "Couches"),
        ("Ducky","Duckies"),
        "Bride",
        "Groom",
        "Daughter",
        "Spider",
        "Dracula",
        "Frankenstein",
        "Godzilla",
        "Dragon",
        "Thunder",
        "Football",
        "Shoe",
        "Winner",
        "Loser"
    ],
    "adjective" : [
        "Tenacious",
        "Flaming",
        "Ordinary",
        "Smart",
        "Fantastic",
        "Raging",
        "Designated",
        "Glorious",
        "Injured",
        "Insane",
        "Blessed",
        "Cursed",
        "Punished",
        "Random",
        "Extraordinary",
        "Bloody",
        "Skilled",
        "Amazing",
        "Super",
        "Bad",
        "Evil",
        "Good",
        "Neutral",
        "Lawful",
        "Chaotic",
        "Undead",
        "Zombie",
        "Vampire",
        "Electric",
        "Eclectic",
        "Eccentric",
        "Indominable",
        "Sideways",
        "Upside-down",
        "Underrated",
        "Overrated",
        "Dependable",
        "Unpredictable"
    ],
}

def nouns(n=1, p=False):
    nnouns = sample(TEAM_NAME_PARTS["noun"],n)
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
    return sample(TEAM_NAME_PARTS["adjective"],n)

def adj():
    return adjs(n=1)[0]

TEAM_NAME_FORMS = [
    lambda: "The {} {}".format(adj(), noun(p=True)), # The Flaming Flamingos
    lambda: "{}{}".format(noun(), noun(p=True).lower()), # Thunderpants
    lambda: "{} {}".format(*nouns(n=2)), # Monkey Python
    lambda: "{} {} {}".format(*(adjs(n=2)+nouns())) # Tenacious Raging Bells
]

def generate_teamnames(nteams):
    teamnames = [generate_teamname() for i in range(nteams)]
    return teamnames

def generate_teamname():
    r = random()
    if r < 0.1:
        return choice(TEAM_NAMES)
    elif r < 0.9:
        return choice(TEAM_NAME_FORMS)()
    else:
        return decorate_teamname(generate_teamname())

def decorate_teamname(name):
    return choice(TEAM_NAME_DECORATIONS)(name)
