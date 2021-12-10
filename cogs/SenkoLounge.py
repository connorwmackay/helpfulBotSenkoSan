import discord
from discord.ext import commands
from cogs import Cog
from googleapiclient.discovery import build
import praw
import random
import os
import httplib2

random.seed()

lounge_name = "Senko's Music Lounge"

class SenkoLounge(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.http = httplib2.Http(cache=".cache")
        self.gservice = build('youtube', 'v3', http=self.http, developerKey=os.getenv('YOUTUBE_API_KEY'))

    def get_random_video(self):
        pass

    @commands.command(name="create")
    async def create_lounge(self, ctx: commands.Context, role_name: str):
        guild: discord.Guild = self.bot.get_guild(ctx.guild.id)
        for channel in guild.channels:
            if channel.name == lounge_name:
                await ctx.send("Channel already exists")
                return

        senko_lounge: discord.VoiceChannel = await guild.create_voice_channel(name=lounge_name)
        await ctx.send("Created voice channel {0}".format(senko_lounge))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if after.channel is not None:
            if after.channel.name == lounge_name and not after.mute:
                await member.edit(mute=True)

    @commands.command(name="play")
    async def play(self):
        pass


def setup(bot):
    bot.add_cog(SenkoLounge(bot))