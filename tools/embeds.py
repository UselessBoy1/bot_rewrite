import discord
from tools import config, misc

permission_denied = discord.Embed(title="Nie masz uprawnien!", color=config.v["CONFIG_COLOR"])

not_in_voice_channel = discord.Embed(title="Musisz byc na kanale glosowym!", color=config.v["CONFIG_COLOR"])

channel_not_mentioned = discord.Embed(title="Musisz oznaczyc kanal <#ID>", color=config.v["CONFIG_COLOR"])

school_class_cmd_on_different_channel = discord.Embed(title="Komenda klasy na kanale innym niz klasowy!", color=config.v['LINK_COLOR'])

def err(color_name="config", reason=""):
    key = f"{color_name.upper()}_COLOR"
    if key not in config.v.keys():
        misc.log(f"ERR: Color named {color_name.upper()}_COLOR doesnt exist")
        key="CONFIG_COLOR"
    out = discord.Embed(title="ERR", color=config.v[key])
    if reason == "":
        return out
    else:
        out.description=reason
        return out
