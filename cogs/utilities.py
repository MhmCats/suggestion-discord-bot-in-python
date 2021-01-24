import discord
from discord.ext import commands

import time
import math
import datetime

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

    async def send_answer(self, ctx, expression, answer):
        embed = discord.Embed(color=discord.Colour.gold(),
                              description=f":inbox_tray: **Input:** ```py\n{expression}```\n:outbox_tray: **Output:** ```fix\n{answer}```")
        embed.set_author(name=ctx.message.author,
                         icon_url=ctx.message.author.avatar_url)
        await ctx.message.reply(embed=embed)
    
    @commands.command(name="calculate")
    async def _calculate(self, ctx, *, expression):
        if await self.check_calculation(list(expression)):
            if len(str(eval(expression))) > 200:
                expression_ans = "Infinty"
            else:
                expression_ans = eval(expression)
            await self.send_answer(ctx, expression, expression_ans)         
        else:
            if "sqrt" in expression and expression.startswith("sqrt(") and expression.endswith(")"):
                number = expression.strip("sqrt()")
                await self.send_answer(ctx, expression, math.sqrt(int(number)))
            else:
                await ctx.send("Your expression had an invalid character in it!")

    @commands.command(name="ping")
    async def _ping(self, ctx):
        t0 = time.time()
        message = await ctx.message.reply("Pong!")
        await message.edit(content=f"**API:** {int(self.bot.latency*1000)}ms\n**Edit Message:** {int((time.time()-t0)*1000)}ms")
    
    async def get_badges(self, user):
        flags = user.public_flags
        badges = {
            "partner": "<:partner:802519060046807040>",
            "hypesquad": "<:hypesquad_events:802520390836158485>",
            "hypesquad_bravery": "<:bravery:802518720215515147>",
            "hypesquad_brilliance": "<:brilliance:802518820224630784>",
            "hypesquad_balance": "<:balance:802518667996037120>",
            "verified_bot_developer": "<:bot_developer:802518905562071101>"
        }
        text = ""
        if flags.hypesquad_balance:
            text += f'{badges["hypesquad_balance"]} '
        if flags.hypesquad_bravery:
            text += f'{badges["hypesquad_bravery"]} '
        if flags.hypesquad_brilliance:
            text += f'{badges["hypesquad_brilliance"]} '
        if flags.verified_bot_developer:
            text += f'{badges["verified_bot_developer"]} '
        if flags.hypesquad:
            text += f'{badges["hypesquad"]} '
        if flags.partner:
            text += f'{badges["partner"]} '
        if not user.premium_since is None:
            text += '<:booster:802519275273322547> '
        if not text == "":
            return text
        else:
            return "None"

    @commands.command(name="userinfo")
    async def _userinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author

        status_types = {
            "online": "<:status_online:802082984059994113>",
            "offline": "<:status_offline:802082948869914654> ",
            "idle": "<:status_idle:802082902564143164>",
            "dnd": "<:status_dnd:802082862077444106>"
        }

        roles = f"{ctx.guild.default_role}, "
        for role in user.roles:
            if not role.id == ctx.guild.id:
                roles += f"<@&{role.id}>, "
            else:
                continue
        roles = roles[:-2]
        
        now = datetime.datetime.now()
        joined_at = f"{user.joined_at.strftime('%d/%m/%Y at %H:%M')} ({(now - user.joined_at).days} days ago)"
        created_at = f"{user.created_at.strftime('%d/%m/%Y at %H:%M')} ({(now - user.created_at).days} days ago)"

        embed = discord.Embed(color=user.color)
        embed.set_author(name=user,
                         icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)

        embed.add_field(name="ID",
                        value=user.id)
        embed.add_field(name="Status",
                        value=f"{status_types[user.raw_status]}")
        embed.add_field(name="Badges",
                        value=await self.get_badges(user))
        embed.add_field(name="Dates",
                        value=f"**Created At:** {created_at}\n**Joined At:** {joined_at}",
                        inline=False)
        embed.add_field(name="Roles",
                        value=roles,
                        inline=False)
        await ctx.message.reply(embed=embed)
    
    @commands.command(name="invite")
    async def _invite(self, ctx):
        embed = discord.Embed(color=discord.Colour.gold(), 
                              description="To invite the bot to your server with the recommended permissions click [here](https://discord.com/api/oauth2/authorize?client_id=743435729085923379&permissions=805694544&scope=bot)"
                                          "\nTo invite the bot with no permissions then click [here](https://discord.com/api/oauth2/authorize?client_id=743435729085923379&permissions=0&scope=bot)")
        embed.set_author(name=ctx.author,
                         icon_url=ctx.author.avatar_url)
        await ctx.message.reply(embed=embed)

def setup(bot):
    bot.add_cog(Utilities(bot))