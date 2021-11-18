import discord

from discord.ext import commands
from tools import permissions, misc, database, config, help, embeds

class DatabaseBot(commands.Cog):

    def __init__(self, bot :commands.Bot):
        self.bot = bot
        self.db = database.Database()


    @commands.command(name="sql")
    @commands.check(permissions.is_dev)
    async def sql_cmd(self, ctx, *args):
        if help.is_it_help(args):
            await ctx.send(embed=help.get_help_embed(self.bot, "sql"))
            return

        cmd = " ".join(args)
        results = self.db.execute(cmd)
        text = ""
        max_chars = 1990
        for r in results:
            max_chars -= len(str(r))
            if max_chars < 0:
                text += "..."
                break
            text += str(r) + "\n"
        if len(results) == 0:
            text = "Empty"
        await ctx.send(text)

    @commands.command(name="show_table")
    @commands.check(permissions.is_dev)
    async def show_table_cmd(self, ctx, *args):
        if help.is_it_help(args):
            await ctx.send(embed=help.get_help_embed(self.bot, "show_table"))
            return

        if len(args) > 0:
            name = args[0]
            try:
                results = self.db.get_table(name)
                embed = discord.Embed(title="RESULTS", description="", color=config.v["CONFIG_COLOR"])
                for r in results:
                    embed.description += str(r) + "\n"
                await ctx.send(embed=embed)
            except Exception as e:
                if hasattr(e, 'message'):
                    await ctx.send(embed=embeds.err(reason=e.message))
                else:
                    await ctx.send(embed=embeds.err())
        else:
            await ctx.send(embed=embeds.err(reason="No <table name>"))

    @commands.command(name="config")
    @commands.check(permissions.is_dev)
    async def config_cmd(self, ctx, *args):
        if help.is_it_help(args):
            await ctx.send(embed=help.get_help_embed(self.bot, "config"))
            return

        if len(args) == 3:
            col_name, new_value, is_int = args
            table = misc.resolve_config_table(self.db.get_table("config"))

            if col_name not in table.keys():
                self.db.add_to_table("config", "namex, valuex, isint", f"'{col_name}', '{new_value}', {is_int}")
                await ctx.send(embed=discord.Embed(title="Added", description=f"'{col_name}', '{new_value}', {is_int}", color=config.v['CONFIG_COLOR']))
            else:
                self.db.replace_in_table("config", ['valuex', 'isint'], [f"'{new_value}'", int(is_int)], where=f"namex = '{col_name}'")
                await ctx.send(embed=discord.Embed(title="Updated", description=f"'{col_name}', '{new_value}', {is_int}", color=config.v['CONFIG_COLOR']))

            config.check_database()

        elif len(args) == 1:
            table = misc.resolve_config_table(self.db.get_table("config"))
            if args[0] in table.keys():
                self.db.delete_from_table("config", f"namex = '{args[0]}'")
                await ctx.send(embed=discord.Embed(title=f"{args[0]} set to default", color=config.v['CONFIG_COLOR']))
            else:
                await ctx.send(embed=discord.Embed(title="Already default", color=config.v['CONFIG_COLOR']))
            config.check_database()

        elif len(args) == 0:
            embed = discord.Embed(title="CONFIG", description="", color=config.v['CONFIG_COLOR'])
            for key in config.v.keys():
                embed.description += str(key) + "\n"
            await ctx.send(embed=embed)

        else:
            await ctx.send(embed=embeds.err("config"))


def setup(bot :commands.Bot):
    bot.add_cog(DatabaseBot(bot))