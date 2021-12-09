import os
import discord
import typing
from unbelieva import Client
from tools.errors import *

client = Client(os.environ['UNBELIVA'])

async def take_money(guild :discord.Guild, user: discord.User, money: int, reason: typing.Optional[str]) -> None:
    user_cash = (await client.get_balance(guild, user)).cash
    if user_cash < money:
        raise NotEnoughMoney

    await client.edit_balance(guild, user, cash=-1)

