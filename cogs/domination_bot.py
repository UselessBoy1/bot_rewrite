import discord
import traceback
import random
import sys
import time
import json

from discord.ext import commands, tasks
from tools import database, permissions, misc, lang, help, config, embeds, encryption

class DominationBot(commands.Cog):
    members_ids_banned_from_voice = []
    members_ids_to_fuck_with = []

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def resolve_voice_cmd(self, args: list) -> list[int]:
        res = []
        for arg in args:
            str_arg = str(arg)
            try:
                if str_arg.startswith("<@!") and str_arg.endswith(">"):
                    member_id = int(str_arg.replace("<@!", "").replace(">", ""))
                    res.append(member_id)
                else:
                    res.append(int(arg))
            except:
                res.append(None)
        return res

    @commands.Cog.listener("on_voice_state_update")
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            if member.id in self.members_ids_banned_from_voice:
                await member.move_to(None)

    @commands.command("voice_ban")
    async def voice_ban_cmd(self,ctx, *args):
        if not permissions.check_permission(ctx, 'ADMIN'):
            await ctx.send(embeds.permission_denied)
            return
        if help.is_it_help(args):
            await ctx.send(embed=help.get_help_embed(self.bot, "voice_ban"))
            return
        members_ids = self.resolve_voice_cmd(list(args))
        banned = []
        for member_id in members_ids:
            if member_id not in self.members_ids_banned_from_voice:
                try:
                    member = ctx.guild.get_member(member_id)
                    if member is None:
                        continue
                    if misc.in_voice_channel(member):
                        await member.move_to(None)
                    banned.append(str(member))
                    self.members_ids_banned_from_voice.append(member_id)
                except:
                    pass
        if len(banned) == 0:
            banned.append("No one :( Args were invalid")
        embed = discord.Embed(title="Voice banned", description=", ".join(banned), color=config.v['CONFIG_COLOR'])
        await ctx.send(embed=embed)


    @commands.command("voice_unban")
    async def voice_unban_cmd(self,ctx, *args):
        if not permissions.check_permission(ctx, 'ADMIN'):
            await ctx.send(embeds.permission_denied)
            return
        if help.is_it_help(args):
            await ctx.send(embed=help.get_help_embed(self.bot, "voice_unban"))
            return
        members_ids = self.resolve_voice_cmd(list(args))
        unbanned = []
        for member_id in members_ids:
            try:
                member = ctx.guild.get_member(member_id)
                if member is None:
                    continue
                self.members_ids_banned_from_voice.remove(member_id)
                unbanned.append(str(member))
            except:
                pass
        if len(unbanned) == 0:
            unbanned.append("No one :) Args were invalid")
        embed = discord.Embed(title="Voice unbanned", description=", ".join(unbanned), color=config.v['CONFIG_COLOR'])
        await ctx.send(embed=embed)

    @commands.command("see_voice_bans")
    async def see_voice_bans_cmd(self, ctx):
        if not permissions.check_permission(ctx, 'ADMIN'):
            await ctx.send(embeds.permission_denied)
            return
        banned = []
        for member_id in self.members_ids_banned_from_voice:
            member = ctx.guild.get_member(member_id)
            if member is None:
                continue
            banned.append(str(member))
        if len(banned) == 0:
            banned.append("No one :( But u can easily fix it :)")
        embed = discord.Embed(title="Voice banned", description=", ".join(banned), color=config.v['CONFIG_COLOR'])
        await ctx.send(embed=embed)

    @commands.command("fuck")
    async def fuck_cmd(self, ctx, *args):
        if not permissions.check_permission(ctx, 'ADMIN'):
            await ctx.send(embeds.permission_denied)
            return
        if len(args) < 2 or help.is_it_help(args):
            await ctx.send(embed=help.get_help_embed(self.bot, "fuck"))
            return
        times = int(args[0])
        members_ids = self.resolve_voice_cmd(list(args)[1:])
        for i in range(times):
            for member_id in members_ids:
                try:
                    member = ctx.guild.get_member(member_id)
                    if member is None:
                        continue
                    previous = member.voice.channel.id
                    voice = random.choice(ctx.guild.voice_channels)
                    rnd_times = 100
                    while voice.id == previous and rnd_times > 0:
                        voice = random.choice(ctx.guild.voice_channels)
                        rnd_times -= 1
                    if misc.in_voice_channel(member):
                        await member.move_to(voice)
                except:
                    pass
            time.sleep(0.5)
        await ctx.send("Fucked them!")


    @tasks.loop(seconds=10)
    async def check_queue(self):
        await self.bot.wait_until_ready()



def setup(bot):
    bot.add_cog(DominationBot(bot))