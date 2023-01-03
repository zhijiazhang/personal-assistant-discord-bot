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

#bot events 

#executes when bot is logged on and online
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")



#global error catching function
#executes when user inputs a command incorrectly
@bot.event
async def on_command_error(ctx, error):

    # Send a message to the user with a list of available commands
    await ctx.send(f'Invalid command. Type !commands to see a list of available commands.')




#bot commands



@bot.command()
async def commands(ctx):
    """Type: !commands to view list of commands and instructions on how to use them"""
    # Get a dictionary of all the registered commands, where the keys are the command names and the values are the command objects
    commands = bot.all_commands

    # Create a message with the list of commands and their docstrings
    message = 'Here is a list of available commands:\n\n'
    for name, command in commands.items():
        if name != 'help':
            message += f'{command} - {command.help}\n'

    # Format the message as a code block
    message = f'```{message}```'

    # Send the message to the user
    await ctx.send(message)



@bot.command()
async def hello(ctx):
    """Type: !hello for a friendly message"""

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




@bot.command()
async def info(ctx):
    """Type: !info to access secret info"""

    await ctx.send(f"You are {ctx.author}")
    await ctx.send(f"Your Discord ID is {ctx.author.id}")
    await ctx.send(f"This server is {ctx.guild}")
    await ctx.send(f"The server ID is {ctx.guild.id}")
    await ctx.send(f"This current channel is {ctx.channel.name}")
    await ctx.send(f"The channel ID is {ctx.channel.id}")




#remind command

"""
(\d+) matches one or more digits , which corresponds to time value
(hours?|minutes?|seconds?) matches to hours/hour , minutes/minute etc..
"""
time_regex = re.compile(r'in (\d+) (hours?|minutes?|seconds?)')

@bot.command()
async def remind(ctx, *, message: str):
    """Type: !remind [reminder] in [numerical number] [hours/minutes/seconds] to set reminder"""
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
    await ctx.send(f'Okay, I will remind you to "{reminder}" in {value} {unit}')
    
    # Pause for the specified time
    await asyncio.sleep(seconds)
    
    # Send the reminder message
    await ctx.send(f"{ctx.author.mention}, reminding you to {reminder}")



#todo command
#TODO add custom emojis to different tasks 

# Create a dictionary to store the to-do lists for each user
todo_lists = {}

@bot.command()
async def todo(ctx, *, message: str):
    """Type: !todo [add/view/delete/done/clear] [task] to modify and view your to do list """

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

        raise on_command_error
    
    #add the task to the user's to-do list
    if action == 'add':

            #add task with emoji based on context of task
            
            for x in task.split():

                if x.lower() in ('important', 'urgent', 'crucial'):

                    task = "\u2757" + " " + task
                    break

                elif x.lower() in ('breakfast', 'lunch', 'dinner', 'eat',):

                    task = "\U0001F60B" + " " + task
                    break

                elif x.lower() in ('study', 'work', 'project', 'leetcode', 'code'):

                    task = '\U0001F4BB' + " " + task
                    break
                
                elif x.lower() in ('gym', 'run', 'workout', 'practice'):

                    task = "\U0001F3C3" + " " + task
                    break


            todo_lists[ctx.author.id].append(task)
            await ctx.send('Task has been added to your to-do list.')
        
    #show the user their to-do-list
    elif action == 'view':

        #prints if the list is empty
        if len(todo_lists[ctx.author.id]) == 0:

            await ctx.send("Your to-do list is empty")

        else:

            list = "Your to-do list: \n\n" + "\n".join(todo_lists[ctx.author.id])
            list = f'```{list}```'
            
            await ctx.send(list)


    #user wants to delete a task or is done with a task
    elif action == "delete" or action == "done":

        for x in todo_lists[ctx.author.id]:

            if task in x:

                todo_lists[ctx.author.id].remove(x)
                await ctx.send("Task removed successfully!")
                return

        await ctx.send("That task does not exist in your to-do list!")
        await ctx.send("Make sure you are typing the task exactly like the way you added it.")
        
        

    else:
        todo_lists[ctx.author.id] = []
        await ctx.send("Your to-do list has been cleared")


#TODO add custom emojis for tasks in reminders


@bot.command()
async def emoji(ctx):

    test = "This is a reminder"
    
    #exclamation mark emoji
    await ctx.send("\u2757" + test)

    #fitness emoji
    await ctx.send("\U0001F3C3" + test)

    #food emoji
    await ctx.send("\U0001F60B"+ test)

    #study emoji
    await ctx.send('\U0001F4BB' + test)




#magic happens
bot.run(bot_token)