from abc import ABC

# Kinds of behaviors.
INVOKE_BEHAVIOR = 0 # Invoke a command.
WIN_BEHAVIOR = 1 # Win a game.

class Behavior(ABC):
  """Behavior encapsulates behavior observed from users."""

  def __init__(self, kind, user_id):
    self.__kind = kind
    self.__user_id = user_id

  def kind(self):
    return self.__kind

  def user_id(self):
    return self.__user_id
