from .behavior import Behavior, INVOKE_BEHAVIOR

class InvokeBehavior(Behavior):
  def __init__(self, user_id, command_name):
    super().__init__(INVOKE_BEHAVIOR, user_id)
    self.__command_name = command_name

  def command_name(self):
    return self.__command_name
