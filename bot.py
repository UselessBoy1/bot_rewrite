import discord
import os
import traceback
import sys
import asyncio
import platform

from discord_components.client import DiscordComponents
from discord.ext import commands
from os.path import isfile, join
from tools import database, misc, config

if platform.system() == "Windows":
    CMD_PREFIXES = ["t?", "T?"]
else:
    CMD_PREFIXES = ['?', "c?", "C?"]


def get_cogs():
    for f in os.listdir("cogs"):
        if isfile(join("cogs", f)) and not f.startswith("_"):
            yield f.replace(".py", "")


def load_cogs(bot):
    for cog in get_cogs():
        try:
            bot.load_extension("cogs" + "." + cog)
        except Exception as e:
            misc.log(f"Can't load extension: {cog}")
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)


def create_default_tables():
    db = database.Database()
    db.create_table("tasks", "channel_id TEXT, epoch TEXT, lesson TEXT, msg TEXT")
    db.create_table("config", "namex TEXT, valuex TEXT, isint INTEGER")
    db.create_table("reddit", "followed TEXT")
    db.create_table("site", "id INTEGER, type TEXT, valuex TEXT")
    db.create_table("website", "type TEXT, txt TEXT, data TEXT, num INTEGER, site_id TEXT, id TEXT")


async def run_bot_async(loop, q=None):
    asyncio.set_event_loop(loop)

    create_default_tables()

    bot = commands.Bot(command_prefix=CMD_PREFIXES, intents=discord.Intents.all(), help_command=None)
    DiscordComponents(bot)


    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game('https://ika-infa.herokuapp.com/'), status=discord.Status.online)
        misc.log("READY")


    load_cogs(bot)
    token = os.environ["TOKEN"]
    await bot.start(token, bot=True, reconnect=True)


def run_bot(loop, q=None):
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)
    _loop.run_until_complete(run_bot_async(loop, q))
    _loop.close()


if __name__ == "__main__":
    run_bot(asyncio.get_event_loop())
