from .config import Config
from .constants import PRIVILEGED_COMMANDS

class Command:
  """Command encapsulates a command issued by a user and with optional arguments."""

  def __init__(self, user_id, command, args=""):
    self.user_id = user_id
    self.command = command.strip().lower()
    self.args = args

  def allowed(self):
    """Check if user, who wrote command is allowed to execute it."""
    if self.command in PRIVILEGED_COMMANDS:
      return self.user_id in Config.get().privileged_users()
    return True
