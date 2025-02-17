from .command import Command

class SpeakCommand(Command):
  def __init__(self, client, text):
    super().__init__("speak")
    self.client = client
    self.text = text
    self.set_ephemeral(False)

  def execute(self, lookup=None):
    self.client.api_call("chat.postMessage", channel=self.channel(), text=self.text)
    return None
