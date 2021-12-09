import discord
from discord.ext.commands import bot
import asyncpraw
import os

reddit = asyncpraw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'), client_secret=os.getenv('REDDIT_CLIENT_SECRET'), user_agent=os.getenv('REDDIT_USER_AGENT'))
