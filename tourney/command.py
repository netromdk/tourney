class Command:
  """Command encapsulates a command issued by a user and with optional arguments."""

  def __init__(self, user_id, command, args=None):
    self.user_id = user_id
    self.command = command.strip().lower()
    self.args = args
