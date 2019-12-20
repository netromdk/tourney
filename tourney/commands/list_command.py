from .command import Command

from tourney.state import State

class ListCommand(Command):
  def __init__(self):
    super(ListCommand, self).__init__("list")
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    state = State.get()
    participants = state.participants()
    amount = len(participants)
    if amount == 0:
      return "No players have joined yet!"

    response = "List of {} players for game of the day:".format(amount)
    for uid in participants:
      name = lookup.user_name_by_id(uid)
      response += "\n\t{}".format(name)

    if amount < 2:
      response += "\nAt least 2 players are required to create matches."

    return response
