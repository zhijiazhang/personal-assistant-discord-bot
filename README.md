## Personal Assistant Discord Bot

Overview:

A discord bot with the current capabilities: 

`quick remind` prompts the bot to remind user in however many hours/minutes/seconds about a task. 

`daily remind` prompts the bot to remind the user daily about a certain task, for example everyday at 8:45 am : "You have lectures in 15 mins".

`todo list` prompts the bot to keep track of user's to-do list, where user can `add` tasks, `view` to-do list, `delete` tasks, and mark tasks as `complete`. 

`weather` prompts the bot to fetch the user the current weather for the a given city.

## How it was built

The bot is written using Python and utilizes the Discord .py API so the bot can be called upon by the user using commands and events inside a discord server. Certain commands rely on the `asyncio` and `datetime` libraries to calculate elapsed time to for the bot to perform certain tasks, and the `weather` command utilizes the Open Weather Map API by sending requests, fetching data, and sending to user. 

The bot is hosted on repl.it, kept "alive" by a uptime monitoring service, and connected to discord main server through a secret access key. Currently active in 5 servers with over 100+ users!


## Command Demos
[![IMG-1748.jpg](https://i.postimg.cc/RFWKcNsh/IMG-1748.jpg)](https://postimg.cc/LYMJS6MF)

### 2 mins later..
[![IMG-1749.jpg](https://i.postimg.cc/6phrws4W/IMG-1749.jpg)](https://postimg.cc/yDkgXbTt)

### Keep track of my todo list for the day
[![IMG-1750.jpg](https://i.postimg.cc/Vsj52qC1/IMG-1750.jpg)](https://postimg.cc/Hjkpy7zP)

### View todo list at any time!
[![IMG-1751.jpg](https://i.postimg.cc/x8Rf8Pvz/IMG-1751.jpg)](https://postimg.cc/rRDXYxYV)


## Installation and Setup Instructions

1. Paste an invitation link for the bot in your browser and it will prompt you to read terms&condtions etc. Press ok and the bot will now be in your server!
2. To learn about commands, type the command `!commands`, which will open up doc of all the commands and how to properly use them.
3. Enjoy!