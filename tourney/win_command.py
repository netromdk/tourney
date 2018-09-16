from .command import Command
from .win_lose import handle_win_lose

class WinCommand(Command):
  def __init__(self):
    super(WinCommand, self).__init__("win")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    return handle_win_lose(self, lookup)
