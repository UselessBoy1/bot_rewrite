import bot
import asyncio

from threading import Thread
from app.main import app

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    Thread(target=bot.run_bot, args=(loop,))
    app.run()