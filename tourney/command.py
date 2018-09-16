import re
from abc import ABC, abstractmethod

from .config import Config
from .constants import PRIVILEGED_COMMANDS

class Command(ABC):
  """Command encapsulates a command issued by a user and with optional arguments."""

  def __init__(self, name):
    self.__name = name
    self.__user_id = None
    self.__args = ""
    self.__channel = None
    self.__ephemeral = True

  def name(self):
    """Command name."""
    return self.__name

  def user_id(self):
    return self.__user_id

  def set_user_id(self, user_id):
    self.__user_id = user_id

  def args(self):
    return self.__args

  def set_args(self, args):
    self.__args = args

  def channel(self):
    return self.__channel

  def set_channel(self, channel):
    self.__channel = channel

  def ephemeral(self):
    return self.__ephemeral

  def set_ephemeral(self, ephemeral):
    self.__ephemeral = ephemeral

  def allowed(self):
    """Check if user, who wrote command is allowed to execute it."""
    if self.name() in PRIVILEGED_COMMANDS:
      return self.user_id() in Config.get().privileged_users()
    return True

  @abstractmethod
  def execute(self, lookup=None):
    """Action to execute with optinal lookup class instance. Returns response to send or None on
    failure."""
    pass
