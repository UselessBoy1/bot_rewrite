import discord
import traceback
import sys
import json

from discord.ext import commands, tasks
from tools import database, permissions, misc, lang, help, config, embeds, encryption

class DominationBot(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @tasks.loop(seconds=10)
    async def check_queue(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(DominationBot(bot))