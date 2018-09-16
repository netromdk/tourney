from .command import Command

from tourney.state import State

class LeaveCommand(Command):
  def __init__(self):
    super(LeaveCommand, self).__init__("leave")

  def execute(self, lookup=None):
    state = State.get()
    participants = state.participants()
    user_name = lookup.user_name_by_id(self.user_id())

    if self.user_id() not in participants:
      return "{}, you've _not_ joined today's game!".format(user_name)

    state.remove_participant(self.user_id())
    state.save()
    return "{}, you've left today's game!".format(user_name)
