#!/usr/bin/env python3
import os
import time
import re
from slackclient import SlackClient

client = SlackClient(os.environ.get("TOURNEY_BOT_TOKEN"))
bot_id = None
channel_id = None
all_channels = None
all_users = {}
participants = []

DEBUG = False
CHANNEL_NAME = "foosball"
RTM_READ_DELAY = 1 # seconds
COMMAND_REGEX = "!(\\w+)\\s*(.*)"

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
    return user_id
  return all_users[user_id]["name"]

def parse_commands(events):
  for event in events:
    if event["type"] == "message" and not "subtype" in event:
      msg = event["text"]
      m = re.search(COMMAND_REGEX, msg)
      if m:
        return event["user"], m.group(1).lower(), m.group(2).strip()
  return None, None, None

def handle_command(user_id, command, args=None):
  response = None
  user_name = lookup_user_name(user_id)
  command = command.lower()

  if command.startswith("help"):
    response = """
As the foosball bot, I accept the following commands:
  *!help* - Shows this text.
  *!list* - List users that joined game of the day.
  *!join* - Join game of the day.
  *!leave* - Leave game of the day.
"""
  elif command.startswith("list"):
    amount = len(participants)
    if amount == 0:
      response = "No participants have joined yet!"
    else:
      response = "List of {} participants for game of the day:".format(amount)
      for uid in participants:
        name = lookup_user_name(uid)
        response += "\n{}".format(name)
  elif command.startswith("join"):
    if user_id not in participants:
      participants.append(user_id)
      response = "{}, you've joined today's game!".format(user_name)
    else:
      response = "{}, you've _already_ joined today's game!".format(user_name)
  elif command.startswith("leave"):
    if user_id not in participants:
      response = "{}, you've _not_ joined today's game!".format(user_name)
    else:
      participants.remove(user_id)
      response = "{}, you've left today's game!".format(user_name)

  if response is not None:
    client.api_call("chat.postMessage", channel=channel_id, text=response)

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
  global channel_id
  channel_id = lookup_channel_name(CHANNEL_NAME)
  if channel_id is None:
    print("Could not find ID for channel: {}".format(CHANNEL_NAME))
    exit(1)
  print("#{} channel ID: {}".format(CHANNEL_NAME, channel_id))

  # Map user IDs to their info.
  for user in get_users():
    all_users[user["id"]] = user
  print("Detected {} users..".format(len(all_users)))

def repl():
  print("Entering REPL..")
  while True:
    events = client.rtm_read()
    if DEBUG:
      print(events)
    user_id, command, args = parse_commands(events)
    if user_id and command:
      handle_command(user_id, command, args)
    time.sleep(RTM_READ_DELAY)

if __name__ == "__main__":
  connect()
  init()
  repl()
