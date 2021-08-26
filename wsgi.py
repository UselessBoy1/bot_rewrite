import bot
import asyncio

from threading import Thread
from app.main import app
from tools import misc

misc.log("RUNNING SERVER")
loop = asyncio.get_event_loop()
Thread(target=bot.bot_run, args=(loop,)).start()

if __name__ == "__main__":
    app.run()