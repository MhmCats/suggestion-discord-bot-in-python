import discord
from discord.ext import commands, tasks

import os
from dotenv import load_dotenv
load_dotenv()

def get_prefix(bot, message):
    prefixes = ["s!", "s! ", "S!", "S! "]

    return commands.when_mentioned_or(*prefixes)(bot, message)

intitial_extensions = ["cogs.admin",
                       "cogs.suggestions",
                       "cogs.help",
                       "cogs.utilities",
                       "cogs.fun"]

intents = discord.Intents(guilds=True, members=True, bans=False, emojis=False, 
                          integrations=True, webhooks=True, invites=False, voice_states=False,
                          presences=False, messages=True, reactions=True, typing=False)

bot = commands.Bot(command_prefix=get_prefix, 
                   owner_id=737928480389333004, 
                   help_command=None,
                   intents=intents)

if __name__ == "__main__":
    for extension in intitial_extensions:
        bot.load_extension(extension)
        print(f"Loaded extension {extension} successfully")

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def print_when_login(self):
        print(f'\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')


    @commands.Cog.listener("on_guild_join")
    async def message_when_join_guild(self, guild):
        role = await guild.create_role(name="Suggestion Blacklist")
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(f"Hello I am a bot made to do suggestions. My prefix is `s!` and pinging me! I have created a role called <@&{role.id}> for you to add to people who you don't want suggesting. Please do not change the name of this role but you are welcome to give it a new colour.\n\nType s!help for help on commands!")
                break

bot.add_cog(Events(bot))

class Pinger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._pinger.start()

    @tasks.loop(seconds=300.0)
    async def _pinger(self):
        print(f"Ping: {int(self.bot.latency*1000)}ms")
        await bot.change_presence(activity=discord.Game(name=f"Watching out for s!help | Ping: {int(self.bot.latency*1000)}ms"), status=discord.Status.online)
    
    @_pinger.before_loop
    async def _before_pinger(self):
        await self.bot.wait_until_ready()

bot.add_cog(Pinger(bot))

bot.run(os.getenv("TOKEN"))