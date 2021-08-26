import bot
import asyncio
import os

from threading import Thread
from app.main import app

policy = asyncio.get_event_loop_policy()
policy._loop_factory = asyncio.SelectorEventLoop

port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(app_loop)
    loop = asyncio.new_event_loop()
    Thread(target=bot.run_bot, args=(loop,)).start()
    app.run(port=port)