from abc import ABC

# Kinds of behaviors.
INVOKE_BEHAVIOR = 0 # Invoke a command.
JOIN_BEHAVIOR   = 1 # Join a game.
LEAVE_BEHAVIOR  = 2 # Leave a game.
WIN_BEHAVIOR    = 3 # Win a game.
LOSE_BEHAVIOR   = 4 # Lose a game.

class Behavior(ABC):
  """Behavior encapsulates behavior observed from users."""

  def __init__(self, kind, user_id):
    self.__kind = kind
    self.__user_id = user_id

  def kind(self):
    return self.__kind

  def user_id(self):
    return self.__user_id
