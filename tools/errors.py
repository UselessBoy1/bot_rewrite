from discord.ext import commands

class TooManyBadRequests(commands.CommandError):
    pass

class NotEnoughMoney(commands.CommandError):
    def __init__(self, money):
        self.money = money