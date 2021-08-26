import bot
import asyncio

from threading import Thread
from app.main import app

if __name__ == "__main__":
    app_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(app_loop)
    loop = asyncio.new_event_loop()
    Thread(target=bot.run_bot, args=(loop,)).start()
    app.run()