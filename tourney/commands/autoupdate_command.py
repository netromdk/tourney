import os
import subprocess  # nosec
import sys
from tourney.config import Config
from tourney.state import State
from .command import Command

class AutoupdateCommand(Command):
  def __init__(self, client):
    super(AutoupdateCommand, self).__init__("stats")
    self.client = client
    self.set_ephemeral(False)

  # If not running as a service then execute "autoupdate.sh" that will
  # git pull and run tourney.py again. Otherwise, it will run
  # "update.sh" that will git pull only. In both cases this process
  # will exit with code 0. Note that when running as a service it is
  # extected that the service will respawn the process when it is
  # terminated!
  def execute(self, lookup=None):
    self.client.api_call("chat.postMessage", channel=State.get().channel_id(),
                         text="Going offline to auto-update and restart..")
    cwd = os.getcwd()
    script = "autoupdate.sh"
    if not os.path.isfile(os.path.join(cwd, script)):
      print(f"Script {script} not found in {cwd}.")
      return
    if Config.get().running_as_service():
      script = "update.sh"
    subprocess.run(["/bin/sh", script], cwd=cwd)  # nosec # pylint: disable=subprocess-run-check
    sys.exit(0)
