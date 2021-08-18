import discord
import requests
import traceback
import sys
import random

from discord.ext import commands
from tools import database, misc, permissions, config, embeds, help

headers = {
    'authority': 'www.reddit.com',
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

class RedditBot(commands.Cog):

    def __init__(self, bot :commands.Bot):
        self.bot = bot
        self.db = database.Database()

    @staticmethod
    def is_url_image(image_url):
        # allowed formats
        image_formats = ("image/png", "image/jpeg", "image/jpg", "image/gif")
        r = requests.head(image_url)
        if 'content-type' in r.headers:
            # if content-type is in allowed formats
            if r.headers["content-type"] in image_formats:
                return True
        return False

    @staticmethod
    def get_subreddit_posts_json(subreddit :str):
        """
        :param subreddit: only name of subreddit (without r/)
        :return: list of posts (dicts)
        """
        response = requests.get(f'https://www.reddit.com/r/{subreddit}/new.json', headers=headers)
        return response.json()['data']['children']

    async def send_meme(self, ctx):
        try:
            # for random misc.Subreddit object
            r = random.choice(misc.resolve_reddit_table(self.db.get_table("reddit")))
            # get json for that subreddit
            posts = self.get_subreddit_posts_json(r.name)
            while True:
                # get data of rand post (dict)
                post = random.choice(posts)['data']
                # check if every required value is in dict
                missing = misc.check_dict(['url_overridden_by_dest', 'title', 'created_utc'], post)
                if len(missing) > 0:
                    # if no try next post
                    continue

                if self.is_url_image(post['url_overridden_by_dest']):
                    #create embed
                    title = post['title']
                    if len(title) == 0:
                        title = "Title"
                    elif len(title) > 100:
                        title = title[:100]+"..."
                    embed = discord.Embed(title=title, color=config.v['REDDIT_COLOR'])
                    embed.set_image(url=post['url_overridden_by_dest'])
                    await ctx.send(embed=embed)
                    return
                else:
                    #if not try next post
                    continue
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
            await ctx.send(embed=discord.Embed(title="ERR", color=config.v['REDDIT_COLOR']))

    @commands.Cog.listener("on_message")
    async def on_message(self, message :discord.Message):
        if message.author.bot:
            return

        for prefix in self.bot.command_prefix:
            if message.content.startswith(prefix):
                return

        if isinstance(message.channel, discord.channel.DMChannel):
            await self.send_meme(message.channel)

    @commands.command(name="meme")
    async def meme_cmd(self, ctx, *args):
        if help.is_it_help(args):
            await ctx.send(embed=help.get_help_embed(self.bot, "meme"))
            return

        await ctx.message.delete()
        await self.send_meme(ctx)

    @commands.command(name="add_reddit")
    async def add_reddit_cmd(self,ctx, *args):
        if not permissions.check_permission(ctx, "ADMIN"):
            await ctx.send(embed=embeds.permission_denied)
            return
        if help.is_it_help(args):
            await ctx.send(embed=help.get_help_embed(self.bot, "add_reddit"))
            return

        if len(args) > 0:
            name = args[0]
            self.db.add_to_table('reddit', "followed", f"'{name}'")
            await ctx.send(embed=discord.Embed(title="Added", color=config.v['REDDIT_COLOR']))
        else:
            await ctx.send(embed=embeds.err("reddit", "Nie podales nazwy subreddita!"))

    @commands.command(name="del_reddit")
    async def del_reddit_cmd(self, ctx, *args):
        if not permissions.check_permission(ctx, "ADMIN"):
            await ctx.send(embed=embeds.permission_denied)
            return

        if help.is_it_help(args):
            await ctx.send(embed=help.get_help_embed(self.bot, "del_reddit"))
            return

        if len(args) > 0:
            name = args[0]
            self.db.delete_from_table('reddit', f"followed = '{name}'")
            await ctx.send(embed=discord.Embed(title="Deleted", color=config.v['REDDIT_COLOR']))
        else:
            await ctx.send(embed=embeds.err("reddit", "Nie podales nazwy subreddita!"))

    @commands.command(name="show_reddit")
    async def show_reddit_cmd(self, ctx, *args):
        if not permissions.check_permission(ctx, "ADMIN"):
            await ctx.send(embed=embeds.permission_denied)
            return

        if help.is_it_help(args):
            await ctx.send(embed=help.get_help_embed(self.bot, "show_reddit"))
            return

        embed = discord.Embed(title="Reddit", description="", color=config.v['REDDIT_COLOR'])
        table = misc.resolve_reddit_table(self.db.get_table('reddit'))
        for t in table:
            embed.description += str(t.name) + "\n"
        await ctx.send(embed=embed)


def setup(bot :commands.Bot):
    bot.add_cog(RedditBot(bot))