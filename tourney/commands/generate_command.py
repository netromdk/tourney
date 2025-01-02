from tourney.state import State
from tourney.match_scheduling import create_matches
from tourney.constants import MATCHMAKING
from tourney.teams import Teams

from random import random

from .command import Command

class GenerateCommand(Command):
  def __init__(self):
    super(GenerateCommand, self).__init__("stats")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    return create_matches(lookup)
