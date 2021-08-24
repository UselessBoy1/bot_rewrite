import discord
import json

from os.path import join, exists
from discord.ext.commands import Bot
from tools.misc import check_dict
from tools import config, misc

def get_help_embed(bot :Bot, cmd):
    path = join("help", "helpcmd.json")
    prefix = bot.command_prefix[0]
    color = config.v['HELP_COLOR']
    if exists(path):
        with open(path) as f:
            data = json.load(f)
        if cmd in data.keys():
            data = data[cmd]
            required = ["description", "fields"]
            missing = check_dict(required, data)
            if len(missing) > 0:
                misc.log(f"Bad json for cmd '{cmd}'! Missing {len(missing)} required values: {', '.join(missing)}")
                return discord.Embed(title="Programista debil", description=f"Zly json, brakuje: {', '.join(missing)}", color=color)
            embed = discord.Embed(title="HELP", description=data["description"].replace("%prefix%", prefix), color=color)
            for f in data["fields"].keys():
                embed.add_field(name=f.replace("%prefix%", prefix), value=data["fields"][f].replace("%prefix%", prefix))
            return embed
        else:
            return discord.Embed(title=f"Nie ma komendy {prefix}{cmd}!", color=color)
    else:
        return discord.Embed(title=f"Programista debil!", description="Nie ma JSONa", color=color)

def is_it_help(args):
    if len(args) == 1:
        if args[0] == "help":
            return True
    return False