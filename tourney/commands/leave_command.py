from tourney.teamname_generator import decorate_teamname
from tourney.state import State
from tourney.achievements import Achievements, LeaveBehavior

from .command import Command

class LeaveCommand(Command):
  def __init__(self):
    super(LeaveCommand, self).__init__("leave")

  def execute(self, lookup=None):
    state = State.get()
    teams = state.teams()
    team_names = state.team_names()
    participants = state.participants()
    dont_remind = state.dont_remind_users()
    user_id = self.user_id()
    user_name = lookup.user_name_by_id(self.user_id())

    # Don't remind user to join before game if user explicitly didn't want to play.
    extra_msg = ""
    if self.user_id() not in dont_remind:
      state.add_dont_remind_user(self.user_id())
      state.save()
      extra_msg = "\nYou won't be reminded later today."

    if any([user_id in t for t in teams]):
      # Let users leave their active team, probably resulting in a 1p team
      new_teams = []
      response = ""
      for team in teams:
        if user_id in team:
          team_index = teams.index(team)
          team_name = team_names[team_index]
          if len(team) > 1:
            new_team_name = decorate_teamname(team_name)
            team_names[team_index] = new_team_name
            new_team = [p for p in team if p != user_id]
            new_teams.append(new_team)

            user_list = ", ".join([lookup.user_name_by_id(uid) for uid in new_team])
            formatted_team_name = "[T{}] *{}*".format(team_index, team_name)
            formatted_new_team_name = "[T{}] *{}* ({})".\
              format(team_index, new_team_name, user_list)

            response += "{}, you have left team\n{}\nwhich becomes\n{}\n".\
              format(user_name, formatted_team_name, formatted_new_team_name)
          elif len(team) == 1:
            response += "{}, you cannot leave team *{}* as its only player\n".\
              format(user_name, team_name)
            response += "Pressure someone else into joining first, then bail.\n"
        else:
          new_teams.append(team)
      response += "Check `!schedule` for overview."
      state.set_teams(new_teams)
      state.set_team_names(team_names)
      state.save()

      # This response must be made public because it changes the team for other players!
      self.set_public(True)

      response += extra_msg
      return response
    elif self.user_id() not in participants:
      return "{}, you've _not_ joined today's game!{}".format(user_name, extra_msg)

    state.remove_participant(self.user_id())
    state.save()
    Achievements.get().interact(LeaveBehavior(self.user_id()))
    return "{}, you've left today's game!{}".format(user_name, extra_msg)
