from discord.ext import commands
from cogs import Cog
import praw
import random
import os
import pytube

from lounge.anime import does_anime_exist

random.seed()


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Memes cog loaded...")

    @commands.command(name="op")
    async def find_op(self, ctx, anime_name: str, season: str = "1"):
        """
        Return a youtube video for the OP of the anime given.
        """
        if not does_anime_exist(anime_name):
            await ctx.send("That anime does not exist. Did you mean any of these?")
            return

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
        if not does_anime_exist(anime_name):
            await ctx.send("That anime does not exist. Did you mean any of these?")
            return

        await ctx.send("Finding ed...")

        yt_video: pytube.YouTube = None
        try:
            yt_video: pytube.YouTube = pytube.Search(anime_name + " ed " + season).results[0]
        except:
            pass

        await ctx.send("{0}".format(yt_video.watch_url))


def setup(bot):
    bot.add_cog(Anime(bot))