import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import datetime
import re

#loads env variable 
load_dotenv()

#get the token for the bot 
bot_token = os.getenv("TOKEN")

#set intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

#creates instance of a bot
bot = commands.Bot(command_prefix="!", description="Personal Assistant Bot",intents=intents)


@bot.event
async def on_ready():
    """prints a message when bot is online"""
    print(f"Logged in as {bot.user}")


#hello command
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

#info command
@bot.command()
async def info(ctx):
    """prints the info of the command in which it was invoked"""

    await ctx.send(f"You are {ctx.author}")
    await ctx.send(f"This server is {ctx.guild}")



#magic happens
bot.run(bot_token)