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

  @abstractmethod
  def achieved(self, user_id):
    """Whether or not user achived the achievement."""
    pass

  @abstractmethod
  def progress(self, user_id):
    """Achievement progress."""
    pass

  @abstractmethod
  def next_tier(self, user_id):
    """Progress to reach for next achievement tier.
    Returns None if no next tier is available."""
    pass

  @abstractmethod
  def tiered_name(self, user_id):
    """Name of the highest achieved achievement name if multi-tiered."""
    pass

  @abstractmethod
  def tiered_description(self, user_id):
    """Description of the highest achieved achievement name if multi-tiered."""
    pass

  def current_progress(self, user_id):
    """Returns formatted string of current progress for user."""
    res = "{}: {}".format(self.tiered_name(user_id), self.tiered_description(user_id))
    nt = self.next_tier(user_id)
    if nt is None:
      if self.achieved(user_id):
        res += " :+1:"
      else:
        res += " :-1:"
    else:
      res += " ({}/{})".format(self.progress(user_id), nt)
    return res
