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



#remind command
#TODO need to implement invalid input error catching

"""
(\d+) matches one or more digits , which corresponds to time value
(hours?|minutes?|seconds?) matches to hours/hour , minutes/minute etc..
"""
time_regex = re.compile(r'in (\d+) (hours?|minutes?|seconds?)')

@bot.command()
async def remind(ctx, *, message: str):
    # Initialize the number of seconds to 0
    seconds = 0
    
    # Iterate through all the matches in the message
    for match in time_regex.finditer(message):
        # Extract the time value and unit from the match
        value = int(match.group(1))
        unit = match.group(2)
        
        # Convert the time value to seconds and add it to the total
        if unit.startswith('hour'):
            seconds += value * 3600
        elif unit.startswith('minute'):
            seconds += value * 60
        elif unit.startswith('second'):
            seconds += value
    
    # Extract the reminder message from the input string
    reminder = time_regex.sub('', message).strip()
  
    # Send a message acknowledging the reminder has been set
    await ctx.send(f'Okay, I will remind you about "{reminder}" in {value} {unit}')
    
    # Pause for the specified time
    await asyncio.sleep(seconds)
    
    # Send the reminder message
    await ctx.send(f"{ctx.author.mention}, reminding you to {reminder}")



#magic happens
bot.run(bot_token)