from .constants import DEMO

class Lookup:
  def __init__(self, client):
    self.__client = client
    self.__all_channels = None
    self.__all_users = {}

  def channel_id_by_name(self, name):
    if DEMO:
      return name
    self.__init_channels()
    for channel in self.__all_channels:
      if channel["name"] == name:
        return channel["id"]
    return None

  def user_name_by_id(self, user_id):
    """Returns display name over name if available."""
    if DEMO:
      return user_id
    self.__init_users()
    if user_id not in self.__all_users:
      return user_id
    info = self.__all_users[user_id]
    if "profile" in info:
      profile = info["profile"]
      dn = profile["display_name"]
      if len(dn) > 0:
        return dn
    return info["name"]

  def __init_channels(self):
    if self.__all_channels is None:
      self.__all_channels = self.__get_channels()

  def __get_channels(self):
    resp = self.__client.api_call("channels.list", exclude_archived=1, exclude_members=1)
    return resp["channels"]

  def __init_users(self):
    if not self.__all_users:
      for user in self.__get_users():
        self.__all_users[user["id"]] = user

  def __get_users(self):
    return self.__client.api_call("users.list")["members"]
