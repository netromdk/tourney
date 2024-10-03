from datetime import datetime

class Season:
  def __init__(self, name, mixin, start_date, end_date):
    self.name = name
    self.mixin = mixin
    self.start_date = start_date
    self.end_date = end_date

  def is_within(self, date):
    date_md = (date.month, date.day)

    if self.start_date <= self.end_date:
      return self.start_date <= date_md <= self.end_date

    # Handle year-end wrap-around
    return date_md >= self.start_date or date_md <= self.end_date

class SeasonChecker:
  __instance = None

  def __init__(self):
    if not SeasonChecker.__instance:
      self.seasons = []
      self.seasons.append(Season('easter', 0.01,
                                 start_date=(3, 1), end_date=(4, 31)))
      self.seasons.append(Season('halloween', 0.1,
                                 start_date=(10, 1), end_date=(10, 31)))
      self.seasons.append(Season('xmas', 0.05,
                                 start_date=(12, 1), end_date=(12, 31)))
      self.seasons.append(Season('pirate_day', 0.1,
                                 start_date=(9, 19), end_date=(9, 19)))
      SeasonChecker.__instance = self

  @staticmethod
  def get():
    if not SeasonChecker.__instance:
      return SeasonChecker()
    return SeasonChecker.__instance

  def get_season(self):
    for season in self.seasons:
      if season.is_within(datetime.now()):
        return season.name
    return None

  def get_seasons(self):
    return self.seasons
