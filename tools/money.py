import os
import discord
import typing
from tools.unbelieva import *
from tools.errors import *

async def take_money(guild :discord.Guild, user: discord.User, money: int, reason: typing.Optional[str]) -> None:
    client = Client(os.environ['UNBELIVA'])
    user_cash = (await client.get_balance(guild, user)).cash
    if user_cash < money:
        raise NotEnoughMoney(money)

    await client.edit_balance(guild, user, cash=-money, reason=reason)

