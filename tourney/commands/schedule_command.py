from tourney.util import schedule_text

from .command import Command

class ScheduleCommand(Command):
  def __init__(self):
    super(ScheduleCommand, self).__init__("schedule")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    return schedule_text(lookup)
