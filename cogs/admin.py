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
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return content.strip('```py\n')

        # remove `foo`
        return content.strip('` \n')

    @commands.is_owner()
    @commands.command(pass_context=True, hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        
        """Evaluates a code"""
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except SystemExit:
            return await ctx.send("I will not do a SystemExit!")
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass
        
    @commands.is_owner()
    @commands.command(hidden=True)
    async def load(self, ctx, *, module):
        try:
            self.bot.load_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'```{e.__class__.__name__}: {e}```')
        else:
            await ctx.message.add_reaction('\u2705')

    @commands.is_owner()
    @commands.command(hidden=True)
    async def unload(self, ctx, *, module):
        try:
            self.bot.unload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'```{e.__class__.__name__}: {e}```')
        else:
            await ctx.message.add_reaction('\u2705')

    @commands.is_owner()
    @commands.group(name='reload', hidden=True, invoke_without_command=True)
    async def _reload(self, ctx, *, module):
        try:
            self.bot.reload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'```{e.__class__.__name__}: {e}```')
        else:
            await ctx.message.add_reaction('\u2705')

def setup(bot):
    bot.add_cog(Admin(bot))