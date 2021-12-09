import os
import discord
import typing
import requests
from unbelieva import Client
from tools.errors import *

client = Client(os.environ['UNBELIVA'])

async def take_money(guild :discord.Guild, user: discord.User, money: int, reason: typing.Optional[str]) -> None:
    user_cash = (await client.get_balance(guild, user)).cash
    if user_cash < money:
        raise NotEnoughMoney

    await client.set_balance(guild, user, cash=user_cash-1000, reason=reason)

