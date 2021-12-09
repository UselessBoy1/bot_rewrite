import os
import discord
import typing
from tools import unbelieva
from tools.errors import *

client = unbelieva.Client(os.environ['UNBELIVA'])

async def take_money(guild :discord.Guild, user: discord.User, money: int, reason: typing.Optional[str]) -> None:
    user_cash = (await client.get_balance(guild, user)).cash
    if user_cash < money:
        raise NotEnoughMoney

    await client.edit_balance(guild, user, cash=user_cash-1000, reason=reason)

