import discord
from discord.ext import commands
from cogs import Cog
from googleapiclient.discovery import build
import praw
import random
import os
import glob
import httplib2
from lounge import lounge
import shutil

from lounge.anime import does_anime_exist, find_closest_anime_matches

random.seed()

lounge_name = "Senko's Music Lounge"


class SenkoLounge(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    def get_random_video(self):
        pass

    @commands.command(name="create")
    async def create_lounge(self, ctx: commands.Context):
        guild: discord.Guild = self.bot.get_guild(ctx.guild.id)
        for channel in guild.channels:
            if channel.name == lounge_name:
                await ctx.send("Channel already exists")
                return

        senko_lounge: discord.VoiceChannel = await guild.create_voice_channel(name=lounge_name)
        await ctx.send("Created voice channel {0}".format(senko_lounge))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        try: # FIXME: Doesn't work when switching from one voice channel to another
            if after.channel is not None:
                # Muting / Unmuting
                if after.channel.name == lounge_name and not after.mute:
                    if member.id != self.bot.user.id:
                        await member.edit(mute=True)
                    else:
                        await member.edit(mute=False)
                elif str(after.channel.name) != lounge_name and after.mute:
                    await member.edit(mute=False)
        except:
            print("A voice-related error occured.")

    @commands.command(name="play")
    async def play(self, ctx, anime_name, type="op", season="1"):
        """
        Play an OP / ED in Senko's Music Lounge.
        :param ctx:
        :param anime_name:
        :param type:
        :param season:
        :return:
        """
        if not does_anime_exist(anime_name):
            # TODO: Add support for reactions, the one, two, or three emojis can be used to play that anime.
            await ctx.send("That anime does not exist.")
            anime_list = find_closest_anime_matches(anime_name)
            anime_options_message = "**Did you mean any of these?**\n"

            for idx, anime in enumerate(anime_list):
                if idx == 0:
                    anime_options_message += ":one:"
                elif idx == 1:
                    anime_options_message += ":two:"
                elif idx == 2:
                    anime_options_message += ":three:"

                anime_options_message += " - {1}\n".format(idx+1, anime.title())

            if len(anime_list) > 0:
                await ctx.send(anime_options_message)
            else:
                await ctx.send("There are no matches.")

            return

        voice_clients: discord.VoiceClient = self.bot.voice_clients
        voice_client = None

        guild: discord.Guild = self.bot.get_guild(ctx.guild.id)
        for channel in guild.channels:
            if channel.name == lounge_name:
                try:
                    voice_client = await channel.connect(reconnect=False)
                except:
                    voice_client = self.bot.voice_clients[0]

                if voice_client.is_playing():
                    pass
                else:
                    shutil.rmtree("./downloads")
                    os.mkdir('./downloads')

                video = lounge.YoutubeVideo("{0} {1} {2}".format(anime_name, type, season))
                video.start_download()

                if voice_client.is_playing():
                    voice_client.stop()

                await ctx.send("Downloading video...")
                audio_source = discord.FFmpegPCMAudio(video.file_path)
                voice_client.play(audio_source)
                await ctx.send("Playing music...")

    @commands.command(name="next")
    async def next(self, ctx):
        """
        Play the next random OP/ED in Senko's Music Lounge.
        :param ctx:
        :return:
        """
        pass


def setup(bot):
    bot.add_cog(SenkoLounge(bot))