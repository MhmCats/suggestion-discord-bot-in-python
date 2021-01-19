import discord
from discord.ext import commands

import time

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    async def check_calculation(self, expression: list):
        operations = ["/", "*", "+", "-", "%", ")", "("]
        for char in expression:
            try: 
                char = int(char)
            except ValueError:
                if not char in operations:
                    return False
                else: 
                    continue
        return True

    @commands.command(name="calculate")
    async def _calculate(self, ctx, *,expression):
        if await self.check_calculation(list(expression)):
            if len(str(eval(expression))) > 200:
                expression_ans = "Infinty"
            else:
                expression_ans = eval(expression)
            embed = discord.Embed(color=discord.Colour.gold(),
                                  description=f":inbox_tray: **Input:** ```py\n{expression}```\n:outbox_tray: **Output:** ```fix\n{expression_ans}```")
            embed.set_author(name=ctx.message.author,
                         icon_url=ctx.message.author.avatar_url)
            await ctx.message.reply(embed=embed)            
        else:
            await ctx.send("Your expression had an invalid character in it!")

    @commands.command(name="ping")
    async def _ping(self, ctx):
        t0 = time.time()
        message = await ctx.message.reply("Pong!")
        await message.edit(content=f"**API:** {int(self.bot.latency*1000)}ms\n**Edit Message:** {int((time.time()-t0)*1000)}ms")

def setup(bot):
    bot.add_cog(Utilities(bot))