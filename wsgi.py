import asyncio
import os
import fallback_bot
import bot
import traceback
import sys

from threading import Thread
from app.main import app
from tools import misc

policy = asyncio.get_event_loop_policy()
policy._loop_factory = asyncio.SelectorEventLoop

port = int(os.environ.get("PORT", 5000))

misc.log(f"Running app on port {port}")

if __name__ == "__main__":
    error_number = 0
    while True:
        try:
            app_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(app_loop)
            loop = asyncio.new_event_loop()
            Thread(target=bot.run_bot, args=(loop,)).start()
            app.run(host="0.0.0.0", port=port)
        except Exception as e:
            error_number += 1
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
            if error_number > 5:
                fallback_bot.run_bot(asyncio.get_event_loop())
