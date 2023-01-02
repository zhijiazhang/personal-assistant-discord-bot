import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import datetime
import re
import random

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



#bot commands


#hello command
@bot.command()
async def hello(ctx):
    # Get the current time
    current_time = datetime.datetime.now()
    
    # Determine the greeting based on the time of day
    if current_time.hour < 12:
        greeting = 'Good morning'
    elif current_time.hour < 18:
        greeting = 'Good afternoon'
    else:
        greeting = 'Good evening'
    
    # Send the greeting to the user
    await ctx.send(f'{greeting}, {ctx.author.mention}!')



#info command
@bot.command()
async def info(ctx):
    """prints the info of the command in which it was invoked"""

    await ctx.send(f"You are {ctx.author}")
    await ctx.send(f"Your Discord ID is {ctx.author.id}")
    await ctx.send(f"This server is {ctx.guild}")
    await ctx.send(f"This current channel is {ctx.channel.name}")




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



#todo command
#TODO write code to catch edge cases 

# Create a dictionary to store the to-do lists for each user
todo_lists = {}

@bot.command()
async def todo(ctx, *, message: str):

    #if the user that called the command is not in the dictionary, add the user to the dictionary 
    if ctx.author.id not in todo_lists:

        todo_lists[ctx.author.id] = []

    #split the message into list of words
    words = message.strip().split()
    
    #check the first word in the command call to determine the action
    action = words[0]
    task = ' '.join(words[1:])
    valid_actions = ['add', 'view', 'delete', 'done', 'clear']
    
    if action not in valid_actions:
        await ctx.send("Invalid Command!")
        await ctx.send("The valid commands are 'add', 'view, 'delete', 'done', 'clear'. ")
        return 
    
    #add the task to the user's to-do list
    if action == 'add':

            #add task 
            todo_lists[ctx.author.id].append(task)
            await ctx.send('Item added to your to-do list')
        
    #show the user their to-do-list
    elif action == 'view':

        #prints if the list is empty
        if len(todo_lists[ctx.author.id]) == 0:

            await ctx.send("Your to-do list is empty")

        else:

            await ctx.send("Your to-do list: \n" + "\n".join(todo_lists[ctx.author.id]))


    #user wants to delete a task or is done with a task
    elif action == "delete" or action == "done":

        if task not in todo_lists[ctx.author.id]:

            await ctx.send("That task does not exist in your to-do list!")
            await ctx.send("Make sure you have the task typed just like the way you added it.")
            return
        

        todo_lists[ctx.author.id].remove(task)
        await ctx.send("Task removed successfully")

    
    else:
        todo_lists[ctx.author.id] = []
        await ctx.send("Your to-do list has been cleared")



#command command
@bot.command()
async def commands(ctx):
    """gives user list of commands and instructions on how to use when called"""

    await ctx.send(

        "!info - calling this command will give information about the user who called the command and server into \n" +

        "!hello - bot will respond with a random friendly greeting depending on time of day"




















    )



#ping command




#magic happens
bot.run(bot_token)