import bot
import asyncio

from threading import Thread
from app.main import app

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    Thread(target=bot.bot_run, args=(loop, )).start()
    app.run()