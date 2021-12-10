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
    async def play(self, ctx, anime_name, type="op", season=1):
        #FIXME: Check if already playing audio, if so stop playing then play new music

        youtube_list_request = self.gservice.search().list(part="snippet", q="{0} {2} {1}".format(anime_name, season, anime_name))
        response = youtube_list_request.execute(http=self.http)

        url = ""

        for video in response["items"]:
            youtube_video_request = self.gservice.videos().list(part="status,player", id=video["id"]["videoId"])
            video_response = youtube_video_request.execute(http=self.http)
            if video_response["items"][0]["status"]["embeddable"]:
                url = "https://www.youtube.com/watch?v={0}".format(video["id"]["videoId"])

        voice_clients: discord.VoiceClient = self.bot.voice_clients
        voice_client = None

        guild: discord.Guild = self.bot.get_guild(ctx.guild.id)
        for channel in guild.channels:
            if channel.name == lounge_name:
                try:
                    voice_client = await channel.connect(reconnect=True)
                except:
                    voice_client = self.bot.voice_clients[0]

                if voice_client.is_playing():
                    voice_client.stop()
                else:
                    shutil.rmtree("./downloads")
                    os.mkdir('./downloads')

                video = lounge.YoutubeVideo(url)
                video.start_download()

                await ctx.send("Downloading video...")
                audio_source = discord.FFmpegPCMAudio(video.file_path)
                voice_client.play(audio_source)
                await ctx.send("Playing music...")


def setup(bot):
    bot.add_cog(SenkoLounge(bot))