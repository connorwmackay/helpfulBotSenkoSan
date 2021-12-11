from discord.ext import commands
from cogs import Cog
from googleapiclient.discovery import build
import praw
import random
import os
import pytube

random.seed()


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Memes cog loaded...")

    @commands.command(name="meme")
    async def find_anime_meme(self, ctx, search_term: str = "", sort_by: str = "", time_filter: str="all"):
        """Find an anime meme from r/Animemes based on the search term
        and return a random submission. Use quotes for the Search Term
        if you want to include multiple words. Sort By and Time Filter are
        both optional parameters, but to use Time Filter Sort By must
        always be present."""
        await ctx.send("Finding meme...")
        subreddit = await Cog.reddit.subreddit('Animemes')

        is_invalid = False

        try:
            search = subreddit.search(query=search_term, sort=sort_by, time_filter=time_filter)
            is_invalid = False
        except:
            is_invalid = True

        if is_invalid:
            try:
                search = subreddit.search(query=search_term, sort=sort_by)
                is_invalid = False
            except:
                is_invalid = True

        if is_invalid:
            try:
                search = subreddit.search(query=search_term)
                is_invalid = False
            except:
                is_invalid = True

        has_sent_msg = False

        search_list = [submission async for submission in search]
        if len(list(search_list)) > 0:
            random_index = random.randint(0, len(list(search_list)) - 1)

            num_iter = 0
            while search_list[random_index].url.find('i.redd.it') == -1:
                if num_iter > 10:
                    await ctx.send("No meme found")
                    return
                random_index = random.randint(0, len(list(search_list)) - 1)
                num_iter += 1

            await ctx.send(search_list[random_index].url)
        else:
            await ctx.send("No meme found")

    @commands.command(name="op")
    async def find_op(self, ctx, anime_name: str, season: str = "1"):
        """
        Return a youtube video for the OP of the anime given.
        """
        await ctx.send("Finding op...")
        yt_video: pytube.YouTube = None
        try:
            yt_video: pytube.YouTube = pytube.Search(anime_name + " op " + season).results[0]
        except:
            pass

        await ctx.send("{0}".format(yt_video.watch_url))

    @commands.command(name="ed")
    async def find_ed(self, ctx, anime_name: str, season: str = "1"):
        """
        Return a youtube video for the ED of the anime given.
        :param ctx:
        :param anime_name:
        :param season:
        :return:
        """
        await ctx.send("Finding ed...")

        yt_video: pytube.YouTube = None
        try:
            yt_video: pytube.YouTube = pytube.Search(anime_name + " ed " + season).results[0]
        except:
            pass

        await ctx.send("{0}".format(yt_video.watch_url))


def setup(bot):
    bot.add_cog(Anime(bot))