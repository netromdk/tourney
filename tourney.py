#!/usr/bin/env python3
import os
from slackclient import SlackClient

client = SlackClient(os.environ.get("TOURNEY_BOT_TOKEN"))
bot_id = None
all_channels = None
all_users = {}

CHANNEL_NAME = "foosball"

def get_channels():
  return client.api_call("channels.list", exclude_archived=1, exclude_members=1)["channels"]

def lookup_channel_name(name):
  for channel in all_channels:
    if channel["name"] == name:
      return channel["id"]
  return None

def get_users():
  return client.api_call("users.list")["members"]

def lookup_user_name(user_id):
  if not user_id in all_users:
    return None
  return all_users[user_id]["name"]

def connect():
  if not client.rtm_connect(with_team_state=False):
    print("Could not connect to Slack!")
    exit(1)

  print("Connected!")

def init():
  bot_id = client.api_call("auth.test")["user_id"]
  print("Tourney bot ID: {}".format(bot_id))

  # Find the channel ID of designated channel name.
  global all_channels
  all_channels = get_channels()
  channel_id = lookup_channel_name(CHANNEL_NAME)
  if channel_id is None:
    print("Could not find ID for channel: {}".format(CHANNEL_NAME))
    exit(1)
  print("#{} channel ID: {}".format(CHANNEL_NAME, channel_id))

  # Map user IDs to their info.
  for user in get_users():
    all_users[user["id"]] = user
  print("Detected {} users..".format(len(all_users)))

if __name__ == "__main__":
  connect()
  init()
