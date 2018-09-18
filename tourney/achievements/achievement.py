from abc import ABC, abstractmethod

class Achievement(ABC):
  """Achievement encapsulates a player's progress to obtain an achievement."""

  def __init__(self, kind):
    self.__kind = kind
    self.data = {} # User ID -> achievement data.

  def kind(self):
    return self.__kind

  def set_data(self, data):
    self.data = data

  @abstractmethod
  def name(self):
    """Name of achievement."""
    pass

  @abstractmethod
  def description(self):
    """Description of achievement."""
    pass

  @abstractmethod
  def accepted_behaviors(self):
    """List of accepted behavior kinds."""
    pass

  def accepts(self, behavior_kind):
    return behavior_kind in self.accepted_behaviors()

  @abstractmethod
  def update(self, behavior):
    """Update achievement progress given behavior.
    Must return True if achievement was obtained, and False otherwise."""
    pass
