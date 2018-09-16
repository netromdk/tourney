from .command import Command
from .win_lose import handle_win_lose

class LoseCommand(Command):
  def __init__(self):
    super(LoseCommand, self).__init__("lose")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    return handle_win_lose(self, lookup)
