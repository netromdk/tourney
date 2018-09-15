import re
from .config import Config
from .constants import COMMAND_REGEX, PRIVILEGED_COMMANDS

class Command:
  """Command encapsulates a command issued by a user and with optional arguments."""

  def __init__(self, user_id, command, args="", channel=None):
    """`user_id` is the command issuer's ID, `command` is the issued command text, `args` is the
optional arguments string, and `channel` is the optional channel the user issued the command
from."""
    self.user_id = user_id
    self.command = command.strip().lower()
    self.args = args
    self.channel = channel

  @staticmethod
  def parse(event):
    """Parse command from RTM event."""
    msg = event["text"].strip()
    m = re.match(COMMAND_REGEX, msg)
    if not m:
      return None
    return Command(user_id=event["user"], command=m.group(1), args=m.group(2).strip(), \
      channel=event["channel"])

  def allowed(self):
    """Check if user, who wrote command is allowed to execute it."""
    if self.command in PRIVILEGED_COMMANDS:
      return self.user_id in Config.get().privileged_users()
    return True
