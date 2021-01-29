import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def print_when_login(self):
        print(f'\nLogged in as: {self.bot.user.name} - {self.bot.user.id}\nVersion: {discord.__version__}\n')
        await self.bot.change_presence(activity=discord.Game(name=f"Watching out for s!help"), status=discord.Status.online)


    @commands.Cog.listener("on_guild_join")
    async def join_guild(self, guild):
        await guild.create_role(name="Suggestion Blacklist")
        embed = discord.Embed(color=discord.Colour.gold(),
                              description=":tada: **Thank you for inviting me!** :tada:\n\nMy prefix is `s!` and you can run `s!help` if you wish to have more information about my commands.")
        embed.set_author(name="Joined server!",
                         icon_url=guild.me.avatar_url)
        embed.set_footer(text="Created by invalid-user#7804")
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=embed)
                return

    
    @commands.Cog.listener("on_guild_remove")
    async def leave_guild(self, guild):
        pass
    
def setup(bot):
    bot.add_cog(Events(bot))