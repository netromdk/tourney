from .command import Command
from .state import State

class JoinCommand(Command):
  def __init__(self):
    super(JoinCommand, self).__init__("join")

  def execute(self, lookup=None):
    state = State.get()
    participants = state.participants()
    user_name = lookup.user_name_by_id(self.user_id())

    if self.user_id() not in participants:
      state.add_participant(self.user_id())
      state.save()
      return "{}, you've joined today's game!".format(user_name)

    return "{}, you've _already_ joined today's game!".format(user_name)
