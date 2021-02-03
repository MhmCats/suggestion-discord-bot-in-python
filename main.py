import discord
from discord.ext import commands, tasks

import os
from dotenv import load_dotenv
load_dotenv()

def _get_prefix(bot, message):
    prefix = "s!"

    return commands.when_mentioned_or(prefix)(bot, message)

intitial_extensions = ["cogs.admin",
                       "cogs.suggestions",
                       "cogs.help",
                       "cogs.utilities",
                       "cogs.fun",
                       "cogs.events"]

intents = discord.Intents.default()
intents.typing = False
intents.members = True
intents.presences = True

bot = commands.AutoShardedBot(command_prefix=_get_prefix, 
                              owner_id=737928480389333004, 
                              help_command=None,
                              intents=intents)

if __name__ == "__main__":
    for extension in intitial_extensions:
        bot.load_extension(extension)
        print(f"Loaded extension {extension} successfully")

class Pinger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._pinger.start()

    @tasks.loop(seconds=300.0)
    async def _pinger(self):
        print(f"Ping: {int(self.bot.latency*1000)}ms")
    
    @_pinger.before_loop
    async def _before_pinger(self):
        await self.bot.wait_until_ready()

bot.add_cog(Pinger(bot))

bot.run(os.getenv("TOKEN"))
