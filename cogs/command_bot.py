import random

import discord
import traceback
import sys
import json
from discord_components import Button, ButtonStyle, InteractionEventType, Interaction

from discord.ext import commands
from tools import database, permissions, misc, lang, help, config, embeds, encryption

class CommandBot(commands.Cog):

    def __init__(self, bot :commands.Bot):
        self.bot = bot
        self.db = database.Database()


    @staticmethod
    async def try_moving_member_on_ping(message):
        if len(message.mentions) == 1:
            mentioned = message.mentions[0]
            # are both from IKA
            if permissions.is_ika(message.author) and permissions.is_ika(mentioned):
                # are both in voice channel
                if misc.in_voice_channel(message.author) and misc.in_voice_channel(mentioned):
                    # does author have permissions to join channel
                    if permissions.can_access_channel(message.author.voice.channel, message.author):
                        # move author to mentioned member's channel
                        await message.author.move_to(mentioned.voice.channel)

    @commands.command(name="exec")
    async def exec_cmd(self, ctx, *args):
        if not permissions.check_permission(ctx, "ADMIN"):
            await ctx.send(embed=embeds.permission_denied)
            return

        if help.is_it_help(args):
            await ctx.send(embed=help.get_help_embed(self.bot, "exec"))
            return

        cmd = " ".join(args)
        try:
            exec(f"async def __exe_func(self, ctx): {cmd}")
            await locals()['__exe_func'](self, ctx)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__, sys.stderr)
            await ctx.send(f"Err {e}")

    @commands.command(name="move")
    async def move_cmd(self, ctx :commands.Context, *args):
        if not permissions.check_permission(ctx, "STRAZNIK"):
            await ctx.send(embed=embeds.permission_denied)
            return

        if help.is_it_help(args):
            await ctx.send(embed=help.get_help_embed(self.bot, "move"))
            return

        if not misc.in_voice_channel(ctx.message.author):
            await ctx.send(embed=embeds.not_in_voice_channel)
            return

        ch_mentions = ctx.message.channel_mentions
        if len(ch_mentions) == 0:
            await ctx.send(embed=embeds.channel_not_mentioned)
            return

        channel = ch_mentions[0]
        if type(channel) != discord.VoiceChannel:
            await ctx.send(embed=discord.Embed(title="ERR"))
            return

        for member in ctx.author.voice.channel.members:
            await member.move_to(channel)
        misc.log(f"Moved {', '.join(member.name for member in ctx.author.voice.channel.members)} to channel '{channel.name}' [{channel.id}]")

    @commands.command(name="dhelp")
    async def dhelp_cmd(self, ctx, *args):
        if len(args) > 0:
            if not permissions.check_permission(ctx, args[0]):
                await ctx.send(embed=embeds.permission_denied)
                return

            if help.is_it_help(args):
                await ctx.send(embed=help.get_help_embed(self.bot, "dhelp"))
                return

            lvl = permissions.get_permission_lvl(args[0])
            embed = discord.Embed(title="HELP", color=config.v['HELP_COLOR'])
            with open("help/helpcmd.json") as f:
                data = json.load(f)
            for cmd in self.bot.commands:
                missing = misc.check_dict([cmd.name], data)
                if len(missing) > 0:
                    misc.log(f"Missing command in help! {cmd}!")
            for cmd in data.keys():
                missing = misc.check_dict(["protection", "brief"], data[cmd])
                if len(missing) > 0:
                    misc.log(f"Missing values: {', '.join(missing)} for {cmd}")
                    continue
                if lvl >= permissions.get_permission_lvl(data[cmd]['protection']):
                    prefix = self.bot.command_prefix[0]
                    embed.add_field(name=prefix + cmd, value=data[cmd]["brief"].replace("%prefix%", prefix), inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embeds.err())

    @commands.command(name="help")
    async def help_cmd(self, ctx, *args):
        if len(args) == 0:
            embed = discord.Embed(title="HELP", color=config.v['HELP_COLOR'])
            with open("help/helpcmd.json") as f:
                data = json.load(f)
            for cmd in self.bot.commands:
                missing = misc.check_dict([cmd.name], data)
                if len(missing) > 0:
                    misc.log(f"Missing command in help! {cmd}!")
            for cmd in data.keys():
                missing = misc.check_dict(["protection", "brief"], data[cmd])
                if len(missing) > 0:
                    misc.log(f"Missing values: {', '.join(missing)} for {cmd}")
                    continue
                if permissions.check_permission(ctx, data[cmd]['protection']):
                    prefix = self.bot.command_prefix[0]
                    embed.add_field(name=prefix+cmd, value=data[cmd]["brief"].replace("%prefix%", prefix), inline=False)

        else:
            embed = help.get_help_embed(self.bot, str(args[0]))
        await ctx.send(embed=embed)

    @commands.command(name="admin")
    async def give_admin(self, ctx, *args):
        if not permissions.check_permission(ctx, 'ADMIN'):
            await ctx.send(embeds.permission_denied)
            return
        if len(ctx.message.mentions) == 1:
            mentioned = ctx.message.mentions[0]
            role_id = permissions.permissions_roles["PRZEWODNICZACY"]
            if not permissions.has_role(role_id, mentioned):
                role = ctx.guild.get_role(role_id)
                await mentioned.add_roles(role)
        else:
            await ctx.send(embeds.err("CONFIG_COLOR", "No member mentioned!"))

    @commands.command(name="detect")
    async def detect_cmd(self, ctx, *args):
        text = " ".join(args)
        await ctx.send(embed=discord.Embed(title=lang.detect_lang(text)[0], color=config.v['CONFIG_COLOR']))

    @commands.command(name="bruh")
    async def bruh_cmd(self, ctx):
        await ctx.message.delete()
        await ctx.send(
            "BRUH",
            components=[
                Button(style=random.randint(1,4), label="BRUH x1",id="bruh.1"),
            ]
        )

    @commands.Cog.listener("on_button_click")
    async def on_button_clicked(self, interaction):
        try:
            interaction_type, data = interaction.component.id.split('.')
            if interaction_type == 'bruh':
                num = int(data) + 1
                await interaction.edit_origin(
                    components=[
                        Button(style=random.randint(1,4), label=f"BRUH x{num}", id=f"bruh.{num}",
                               custom_id=misc.to_hex(discord.Color.random().to_rgb())),
                    ]
                )
                await interaction.respond(type=6)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
            await interaction.send(embed=embeds.err(reason="Something went wrong!"))

    @commands.Cog.listener("on_command_error")
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send(embed=embeds.permission_denied)
        elif isinstance(error, commands.errors.CommandNotFound):
            pass
        else:
            await ctx.send(f"```\n{traceback.format_exception(type(error), error, error.__traceback__)}\n```")


    @commands.Cog.listener("on_message")
    async def on_message(self, message :discord.Message):
        if message.author.bot:
            return
        await self.try_moving_member_on_ping(message)


def setup(bot :commands.Bot):
    cmd_bot = CommandBot(bot)
    bot.add_cog(cmd_bot)