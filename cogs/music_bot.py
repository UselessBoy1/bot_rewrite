import asyncio
import discord
import requests
import typing

from collections import deque
from discord.ext import commands, tasks
from tools import config, misc, embeds

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

HEADERS = {
    'authority': 'invidious.snopyta.org',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Mobile Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'
}


class SearchResult:
    def __init__(self, vid, title, author):
        self.vid = vid
        self.title = title
        self.author = author


class Song:
    def __init__(self, title, author, vformat, vid):
        self.title = title
        self.author = author
        self.vformat = vformat
        self.vid = vid

class PlayerOptions:
    def __init__(self):
        self.song_queue = deque()
        self.voice = None
        self.text_channel = None
        self.playing = False
        self.paused = False
        self.loop = False
        self.now_playing = None

class MusicBot(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.song_players = {}


    @classmethod
    def search(cls, title) -> typing.Optional[SearchResult]:
        response = requests.get(f"https://invidious.snopyta.org/api/v1/search?q={title}&fields=type,title,videoId,author", headers=HEADERS)
        json = response.json()
        for film in json:
            if film['type'] == 'video':
                return SearchResult(film['videoId'], film['title'], film['author'])
        return None


    @classmethod
    def get_format(cls, search_results: SearchResult) -> dict:
        response = requests.get(f"https://invidious.snopyta.org/api/v1/videos/{search_results.vid}?fields=adaptiveFormats", headers=HEADERS)
        af = response.json()['adaptiveFormats']
        for f in af:
            if f['encoding'] == 'opus':
                return f
        return af[0]


    async def play_next(self, guild_id):
        player = self.song_players[guild_id]
        if len(player.song_queue) != 0:
            song = player.song_queue.popleft()
            embed = discord.Embed(
                title=f"Now playing",
                description=f"[{song.title}](https://youtu.be/{song.vid})",
                color=config.v['MUSIC_COLOR']
            )


            await player.text_channel.send(embed=embed)

            if player.loop:
                player.song_queue.append(song)

            player.paused = False

            source = await discord.FFmpegOpusAudio.from_probe(song.vformat['url'], **FFMPEG_OPTIONS)

            player.voice.play(
                source,
                after=lambda e: self.bot.dispatch("play_next", guild_id)
            )

            player.playing = True
            player.now_playing = song
        else:
            player.playing = False
            player.now_playing = None
            player.voice.stop()


    @commands.command(name="play")
    async def play_cmd(self, ctx: commands.Context, *, org_title: str):
        if not misc.in_voice_channel(ctx.author):
            await ctx.send(embed=embeds.not_in_voice_channel)
            return

        search_msg = await ctx.send(embed=discord.Embed(title="Searching...", color=config.v['SEARCH_COLOR']))
        title = '+'.join(org_title.split())
        search_results = self.search(title)

        if search_results is None:
            embed = discord.Embed(
                title=f"Couldn't find '{org_title}'!",
                color=config.v['FAIL_COLOR']
            )
            await ctx.send(embed=embed)
            await search_msg.delete()
            return

        vid_format = self.get_format(search_results)
        player = self.song_players[ctx.guild.id]
        if ctx.voice_client is None or ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.author.voice.channel.connect()
            player.voice = ctx.guild.voice_client
            player.song_queue.clear()
            await asyncio.sleep(0.1)

        player.text_channel = ctx.channel
        player.song_queue.append(Song(search_results.title, search_results.author, vid_format, search_results.vid))
        await search_msg.delete()

        if player.playing:
            embed = discord.Embed(
                title=f"Added to queue",
                description=f"[{search_results.title}](https://youtu.be/{search_results.vid})",
                color=config.v['MUSIC_COLOR']
            )
            await ctx.send(embed=embed)
        else:
            await self.play_next(ctx.guild.id)


    @commands.command(name="queue")
    async def queue_cmd(self, ctx: commands.Context):
        embed = discord.Embed(title="Queue", color=config.v['MUSIC_COLOR'])
        player = self.song_players[ctx.guild.id]
        if player.playing:
            link = f'[{player.now_playing.title}](https://youtu.be/{player.now_playing.vid})'
            if player.paused:
                embed.description = f"Paused {link}\n"
            else:
                embed.description = f"Playing {link}\n"

        i = 1
        for song in player.song_queue:
            embed.description += f"``{i}`` [{song.title}](https://youtu.be/{song.vid})\n"

        if len(player.song_queue) == 0:
            embed.title = "Queue - Empty"

        await ctx.send(embed=embed)


    @commands.command(name="skip")
    async def skip_cmd(self, ctx):
        player = self.song_players[ctx.guild.id]
        if player.playing:
            player.voice.stop()
            await ctx.message.add_reaction("👌")


    @commands.command(name="pause")
    async def pause_cmd(self, ctx):
        player = self.song_players[ctx.guild.id]
        if player.playing and not player.paused:
            player.voice.pause()
            player.paused = True
            await ctx.message.add_reaction('⏸')


    @commands.command(name="resume")
    async def resume_cmd(self, ctx):
        player = self.song_players[ctx.guild.id]
        if player.playing and player.paused:
            player.voice.resume()
            player.paused = False
            await ctx.message.add_reaction('▶')


    @commands.command(name="stop")
    async def stop_cmd(self, ctx: commands.Context):
        player = self.song_players[ctx.guild.id]
        if player.playing:
            player.paused = False
            player.song_queue.clear()
            player.voice.stop()
            await ctx.message.add_reaction("❌")


    @commands.command(name="loop")
    async def loop_cmd(self, ctx):
        player = self.song_players[ctx.guild.id]
        if player.loop:
            await ctx.send(embed=discord.Embed(title="Looping disabled"))
        else:
            await ctx.send(embed=discord.Embed(title="Looping queue"))
            if player.now_playing is not None:
                player.song_queue.append(player.now_playing)
        player.loop = not player.loop

    @commands.Cog.listener("on_play_next")
    async def on_play_next(self, guild_id):
        await self.play_next(guild_id)

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        for guild in self.bot.guilds:
            self.song_players[guild.id] = PlayerOptions()



def setup(bot: commands.Bot):
    bot.add_cog(MusicBot(bot))