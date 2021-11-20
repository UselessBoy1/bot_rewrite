import asyncio
import discord
import requests
import typing

from collections import deque
from discord.ext import commands, tasks
from tools import config, misc, embeds

headers = {
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
    def __init__(self, title, author, vformat):
        self.title = title
        self.author = author
        self.vformat = vformat

class MusicBot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.song_queue = deque()
        self.voice = None
        self.text_channel = None
        self.to_send = None
        self.send_msgs.start()
        self.playing = False
        self.paused = False
        self.loop = False

    @classmethod
    def search(cls, title) -> typing.Optional[SearchResult]:
        response = requests.get(f"https://invidious.snopyta.org/api/v1/search?q={title}&fields=type,title,videoId,author", headers=headers)
        json = response.json()
        for film in json:
            if film['type'] == 'video':
                return SearchResult(film['videoId'], film['title'], film['author'])
        return None

    @classmethod
    def get_format(cls, search_results: SearchResult) -> dict:
        response = requests.get(f"https://invidious.snopyta.org/api/v1/videos/{search_results.vid}?fields=adaptiveFormats", headers=headers)
        return response.json()['adaptiveFormats'][0]

    def play_next(self):
        if len(self.song_queue) != 0:
            video = self.song_queue.popleft()
            embed = discord.Embed(
                title=f"Now playing",
                description=f"{video.title}",
                color=config.v['MUSIC_COLOR']
            )
            self.to_send = embed
            if self.loop:
                self.song_queue.append(video)
            self.voice.play(
                discord.FFmpegPCMAudio(
                    executable="ffmpeg.exe",
                    source=video.vformat['url'],
                    before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                ),
                after=lambda e: self.play_next()
            )
            self.playing = True
        else:
            self.playing = False
            self.voice.stop()



    @commands.command(name="play")
    async def play_cmd(self, ctx: commands.Context, *, org_title: str):
        if not misc.in_voice_channel(ctx.author):
            await ctx.send(embed=embeds.not_in_voice_channel)
            return
        search_msg = await ctx.send(embed=discord.Embed(title="Searching...", color=config.v['MUSIC_COLOR']))
        title = '+'.join(org_title.split())
        search_results = self.search(title)
        if search_results is None:
            embed = discord.Embed(
                title=f"Couldn't find '{org_title}'!",
                color=config.v['MUSIC_COLOR']
            )
            await ctx.send(embed=embed)
            await search_msg.delete()
            return
        vid_format = self.get_format(search_results)
        if ctx.voice_client is None or ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.author.voice.channel.connect()
            self.voice = ctx.guild.voice_client
            self.song_queue.clear()
            await asyncio.sleep(0.1)
        self.text_channel = ctx.channel
        self.song_queue.append(Song(search_results.title, search_results.author, vid_format))
        await search_msg.delete()
        if self.playing:
            embed = discord.Embed(
                title=f"Added to queue",
                description=f"{search_results.title}",
                color=config.v['MUSIC_COLOR']
            )
            await ctx.send(embed=embed)
        else:
            self.play_next()

    @commands.command(name="queue")
    async def queue_cmd(self, ctx: commands.Context):
        embed = discord.Embed(title="Queue", color=config.v['MUSIC_COLOR'])
        for song in self.song_queue:
            embed.add_field(name=f"{song.title}", value=f"{song.author}", inline=False)
        if len(self.song_queue) == 0:
            embed.title = "Queue - Empty"
        await ctx.send(embed=embed)

    @commands.command(name="skip")
    async def skip_cmd(self, ctx):
        if self.playing:
            self.voice.stop()
            await ctx.message.add_reaction("👌")

    @commands.command(name="pause")
    async def pause_cmd_(self, ctx):
        if self.playing and not self.paused:
            self.voice.pause()
            self.paused = True
            await ctx.message.add_reaction('⏸')

    @commands.command(name="resume")
    async def resume_cmd(self, ctx):
        if self.playing and self.paused:
            self.voice.resume()
            self.paused = False
            await ctx.message.add_reaction('▶')

    @commands.command(name="stop")
    async def stop_cmd(self, ctx: commands.Context):
        if self.playing:
            self.song_queue.clear()
            self.voice.stop()
            await ctx.message.add_reaction("❌")

    @commands.command(name="loop")
    async def loop_cmd(self, ctx):
        if self.loop:
            await ctx.send("Loop disabeled")
        else:
            await ctx.send("Looping queue")
        self.loop = not self.loop

    @tasks.loop(seconds=1)
    async def send_msgs(self):
        if self.to_send is not None:
            await self.text_channel.send(embed=self.to_send)
            self.to_send = None


def setup(bot: commands.Bot):
    bot.add_cog(MusicBot(bot))