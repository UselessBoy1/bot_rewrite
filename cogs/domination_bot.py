import discord
import random
import time

from discord.ext import commands, tasks
from tools import database, permissions, misc, lang, help, config, embeds, encryption


class DominationBot(commands.Cog):
    members_ids_banned_from_voice = []
    members_ids_to_fuck_with = []

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #region CMD
    @commands.command("voice_ban")
    @commands.check(permissions.is_admin)
    async def voice_ban_cmd(self,ctx, members: commands.Greedy[discord.Member], flags=""):
        flags = [f.removeprefix('-') for f in flags.split(" ")]
        if help.is_it_help(flags):
            await ctx.send(embed=help.get_help_embed(self.bot, "voice_ban"))
            return
        banned = []
        for member in members:
            if member.id not in self.members_ids_banned_from_voice:
                if member is None:
                    continue
                if misc.in_voice_channel(member):
                    await member.move_to(None)
                banned.append(str(member))
                self.members_ids_banned_from_voice.append(member.id)
        if len(banned) == 0:
            banned.append("No one :( Args were invalid")
        embed = discord.Embed(title="Voice banned", description=", ".join(banned), color=config.v['CONFIG_COLOR'])
        await ctx.send(embed=embed)


    @commands.command("voice_unban")
    @commands.check(permissions.is_admin)
    async def voice_unban_cmd(self,ctx, members: commands.Greedy[discord.Member], flags=""):
        flags = [f.removeprefix('-') for f in flags.split(" ")]
        if help.is_it_help(flags):
            await ctx.send(embed=help.get_help_embed(self.bot, "voice_unban"))
            return
        unbanned = []
        for member in members:
            try:
                if member is None:
                    continue
                self.members_ids_banned_from_voice.remove(member.id)
                unbanned.append(str(member))
            except ValueError:
                pass
        if len(unbanned) == 0:
            unbanned.append("No one :) Args were invalid")
        embed = discord.Embed(title="Voice unbanned", description=", ".join(unbanned), color=config.v['CONFIG_COLOR'])
        await ctx.send(embed=embed)


    @commands.command("see_voice_bans")
    @commands.check(permissions.is_admin)
    async def see_voice_bans_cmd(self, ctx):
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
    @commands.check(permissions.is_admin)
    async def fuck_cmd(self, ctx, times: commands.Greedy[int], members: commands.Greedy[discord.Member], flags=""):
        flags = [f.removeprefix('-') for f in flags.split(" ")]
        if help.is_it_help(flags):
            await ctx.send(embed=help.get_help_embed(self.bot, "fuck"))
            return
        for i in range(times):
            for member in members:
                if member.id == permissions.dev:
                    continue
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
                previous = voice
            time.sleep(0.5)
        await ctx.send("Fucked them!")
    #endregion

    @commands.Cog.listener("on_voice_state_update")
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            if member.id in self.members_ids_banned_from_voice:
                await member.move_to(None)

    @tasks.loop(seconds=10)
    async def check_queue(self):
        await self.bot.wait_until_ready()



def setup(bot):
    bot.add_cog(DominationBot(bot))