#!/usr/bin/env python3
import os
from slackclient import SlackClient

client = SlackClient(os.environ.get("TOURNEY_BOT_TOKEN"))
bot_id = None
all_channels = None

CHANNEL_NAME = "foosball"

def get_channels():
  return client.api_call("channels.list", exclude_archived=1, exclude_members=1)["channels"]

def lookup_channel_name(name):
  for channel in all_channels:
    if channel["name"] == name:
      return channel["id"]
  return None

if __name__ == "__main__":
  if not client.rtm_connect(with_team_state=False):
    print("Could not connect to Slack!")
    exit(1)

  print("Connected!")

  bot_id = client.api_call("auth.test")["user_id"]
  print("Tourney bot ID: {}".format(bot_id))

  # Find the channel ID of designated channel name.
  all_channels = get_channels()
  channel_id = lookup_channel_name(CHANNEL_NAME)
  if channel_id is None:
    print("Could not find ID for channel: {}".format(CHANNEL_NAME))
    exit(1)
  print("#{} channel ID: {}".format(CHANNEL_NAME, channel_id))
