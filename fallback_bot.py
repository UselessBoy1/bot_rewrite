import asyncio
import os
import discord

from discord.ext import commands

CMD_PREFIXES = ["c?", "C?"]

async def run_bot_async(loop):
    asyncio.set_event_loop(loop)

    bot = commands.Bot(command_prefix=CMD_PREFIXES, help_command=None)

    @bot.event
    async def on_ready():
        print("GET READY TO FIX ME :)")
        await bot.change_presence(activity=discord.Game("Im having 500. Pls fix me :)"), status=discord.Status.do_not_disturb)

    token = os.environ["TOKEN"]
    await bot.start(token, bot=True, reconnect=True)

def run_bot(loop):
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)
    _loop.run_until_complete(run_bot_async(loop))
    _loop.close()

if __name__ == "__main__":
    run_bot(asyncio.get_event_loop())