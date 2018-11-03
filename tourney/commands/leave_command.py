from .command import Command

from tourney.state import State
from tourney.achievements import Achievements, LeaveBehavior

class LeaveCommand(Command):
  def __init__(self):
    super(LeaveCommand, self).__init__("leave")

  def execute(self, lookup=None):
    state = State.get()
    participants = state.participants()
    dont_remind = state.dont_remind_users()
    user_name = lookup.user_name_by_id(self.user_id())

    # Don't remind user to join before game if user explicitly didn't want to play.
    extra_msg = ""
    if self.user_id() not in dont_remind:
      state.add_dont_remind_user(self.user_id())
      state.save()
      extra_msg = "\nYou won't be reminded later today."

    if self.user_id() not in participants:
      return "{}, you've _not_ joined today's game!{}".format(user_name, extra_msg)

    state.remove_participant(self.user_id())
    state.save()
    Achievements.get().interact(LeaveBehavior(self.user_id()))
    return "{}, you've left today's game!{}".format(user_name, extra_msg)
