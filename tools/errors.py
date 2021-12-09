from discord.ext import commands

class TooManyBadRequests(commands.CommandError):
    pass

class NotEnoughMoney(commands.CommandError):
    pass