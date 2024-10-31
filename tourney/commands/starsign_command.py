from .command import Command
from .starsigns import Starsigns

class JoinCommand(Command):
  def __init__(self):
    super().__init__("starsign")

  def execute(self, lookup=None):
    starsigns = Starsigns.get()
    new_sign = self.args()
    response = starsigns.add(user_id, new_sign)
