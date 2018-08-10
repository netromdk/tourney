#!/usr/bin/env python3
import os
from slackclient import SlackClient

client = SlackClient(os.environ.get("TOURNEY_BOT_TOKEN"))
bot_id = None

if __name__ == "__main__":
  if not client.rtm_connect(with_team_state=False):
    print("Could not connect to Slack!")
    exit(1)

  print("Connected!")

  bot_id = client.api_call("auth.test")["user_id"]
  print("Tourney bot ID: {}".format(bot_id))
