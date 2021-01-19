# Suggestion Discord Bot Made In Python

This bot was made in the discord.py library which you can install by running either:
* For MacOS and Linux
```python3 -m pip install -U discord.py```
* For Windows
```py -3 -m pip install -U discord.py```

I also used dotenv which can be installed with:
* For MacOS and Linux
```python3 -m pip install -U python-dotenv```
* This might work for Windows
```py -3 -m pip install -U discord.py```

The use of dotenv would be like so:

*The bot's file*
```
import discord
import os

from dotenv import load_dotenv
TOKEN = os.getenv("TOKEN")

client = discord.Client()

client.run(TOKEN)
```

*The .env file*
```
TOKEN=[insert your bot token here]
```

## Main structure

The principle of the suggestion feauture of the bot is that, instead of the bot posting the message directly, it makes a request for a webhook in the #suggestions channel to post the suggestion.

The main point of this was to make it look better as a webhook's name and avatar can be changed every time it posts a new message. In this case the name and avatar would be changed to the person who is making the suggestion.

**Please note that any commands requiring elevated permissions *except from the Owner commands* require permissions of "Manage Server" or higher**

Feel free to copy any of this code
