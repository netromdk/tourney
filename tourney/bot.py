from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity, ActivityTypes
from typing import Callable

def init(app_id: str, app_password: str, message_activity_func: Callable[[Activity], str | list[str]]):
  settings = BotFrameworkAdapterSettings(app_id, app_password)
  adapter = BotFrameworkAdapter(settings)

  async def messages(req: web.Request) -> web.Response:
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    async def on_turn(turn_context: TurnContext):
      if activity.type == ActivityTypes.message:
        resps = await message_activity_func(activity)
        if isinstance(resps, str):
          resps = [resps]
        for resp in resps:
          await turn_context.send_activity(resp)
 
    await adapter.process_activity(activity, auth_header, on_turn)
    return web.Response(status=200)

  app = web.Application()
  app.router.add_post("/api/messages", messages)
  return app

def run(app: web.Application, host: str, port: int):
  web.run_app(app, host=host, port=port)