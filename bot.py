import discord
import os
import traceback
import sys
import threading
import asyncio
import datetime

from discord.ext import commands
from os.path import isfile, join
from tools import database, misc, config

CMD_PREFIXES = ["t?", "T?"]
pending_index = -1

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


if __name__ == "__main__":
    create_default_tables()

    bot = commands.Bot(command_prefix=CMD_PREFIXES, intents=discord.Intents.all(), help_command=None)


    @bot.event
    async def on_ready():
        misc.log("READY")


    @bot.event
    async def on_pending_reminder_set(reminder):
        global pending_index
        pending_index = reminder.index


    load_cogs(bot)
    token = os.environ["TOKEN"]
    bot.run(token, bot=True, reconnect=True)

