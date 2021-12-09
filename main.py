import discord
import os
from dotenv import load_dotenv

load_dotenv()

from cogs.Anime import Anime
from discord.ext import commands

bot = commands.Bot(command_prefix="!senko ")

@bot.event
async def on_ready():
    print('Starting bot...')
    print('Logged in as {0.user}'.format(bot))

bot.load_extension('cogs.Anime')
bot.run(os.getenv('DISCORD_TOKEN'))