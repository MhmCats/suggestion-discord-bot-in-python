import discord
from discord.ext import commands

import io
import textwrap
import traceback
from contextlib import redirect_stdout

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def cleanup_code(self, content):
        if content.startswith('```') and content.endswith('```'):
            return content.strip('```py\n')
        return content.strip('` \n')

    @commands.is_owner()
    @commands.command(pass_context=True, hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        env = {
            '_bot': self.bot,
            'ctx': ctx,
            '_channel': ctx.channel,
            '_author': ctx.author,
            '_guild': ctx.guild,
            '_message': ctx.message
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
        try:
            exec(to_compile, env)
        except Exception as e:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description=f'```py\n{e.__class__.__name__}: {e}\n```')
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.send(embed=embed)

        func = env['func']
        try:
            with redirect_stdout(stdout):
                await func()
        except SystemExit:
            return
        except Exception as e:
            value = stdout.getvalue()
            embed = discord.Embed(color=discord.Colour.red(),
                                  description=f'```py\n{value}{traceback.format_exc()}\n```')
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            await ctx.send(embed=embed)
        else:
            value = stdout.getvalue()
            try:
                emoji = "<:yes:802083268098785291>"
                await ctx.message.add_reaction(emoji)
            except:
                pass
        
    @commands.is_owner()
    @commands.command(hidden=True)
    async def load(self, ctx, *, module):
        try:
            self.bot.load_extension(module)
        except commands.ExtensionError as e:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description=f'```py\n{e.__class__.__name__}: {e}\n```')
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.send(embed=embed)
        else:
            emoji = "<:yes:802083268098785291>"
            await ctx.message.add_reaction(emoji)

    @commands.is_owner()
    @commands.command(hidden=True)
    async def unload(self, ctx, *, module):
        try:
            self.bot.unload_extension(module)
        except commands.ExtensionError as e:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description=f'```py\n{e.__class__.__name__}: {e}\n```')
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.send(embed=embed)
        else:
            emoji = "<:yes:802083268098785291>"
            await ctx.message.add_reaction(emoji)

    @commands.is_owner()
    @commands.group(name='reload', hidden=True, invoke_without_command=True)
    async def _reload(self, ctx, *, module):
        try:
            self.bot.reload_extension(module)
        except commands.ExtensionError as e:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description=f'```py\n{e.__class__.__name__}: {e}\n```')
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.send(embed=embed)
        else:
            emoji = "<:yes:802083268098785291>"
            await ctx.message.add_reaction(emoji)

def setup(bot):
    bot.add_cog(Admin(bot))