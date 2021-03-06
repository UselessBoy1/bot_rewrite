import discord
from tools import config, misc

permission_denied = discord.Embed(title="Nie masz uprawnien!", color=config.v["FAIL_COLOR"])

command_not_found = discord.Embed(title="Nie ma takiej komendy!", color=config.v['FAIL_COLOR'])

not_in_voice_channel = discord.Embed(title="Musisz byc na kanale glosowym!", color=config.v['FAIL_COLOR'])

channel_not_mentioned = discord.Embed(title="Musisz oznaczyc kanal <#ID>", color=config.v["FAIL_COLOR"])

school_class_cmd_on_different_channel = discord.Embed(title="Komenda klasy na kanale innym niz klasowy!", color=config.v['LINK_COLOR'])

too_many_bad_requests = discord.Embed(title="Bot ma za duzo BadRequest do API. Funkcja zostala chwilowo wylaczona", color=config.v['FAIL_COLOR'])

def not_enough_money(money: int, icon):
    return discord.Embed(title=f"Nie masz pieniedzy", description=f"Potrzebujesz {icon} {money}", color=config.v['FAIL_COLOR'])

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
