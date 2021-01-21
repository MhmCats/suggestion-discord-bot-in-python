import discord
from discord.ext import commands

import asyncio
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hack")
    async def _hack(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author

            message = await ctx.send("You didn't provide anyone to hack...")
            await asyncio.sleep(3)
            await message.edit(content="Never mind I will hack you instead")
            await asyncio.sleep(1)
            await message.delete()
        
        words = ["pog", "lol", "e", "lmao", "hehe"]
        games = ["fortnite", "minecraft", "roblox", "rocket league", "fnaf"]

        message = await ctx.send(f"```Hacking {user}...\n\nETA: 11s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Grabbing Token... \n\nETA: 10s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Downloading friends list \n\nETA: 9s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Found most said word: {random.choice(words)} \n\nETA: 8s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Calculating age \n\nETA: 7s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Found age: {random.randint(13, 35)} \n\nETA: 6s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Spamming in every server... \n\nETA: 5s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Got banned for spamming in every server... \n\nETA: 4s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Unbanning myself \n\nETA: 3s```")
        await asyncio.sleep(1) 
        await message.edit(content=f"```Favourite game: {random.choice(games)} \n\nETA: 2s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Spreading Trojan Viruses \n\nETA: 1s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Finished Hacking {user} \n\nETA: Done!```")

    @commands.command(name="calmly")
    async def _calmly(self, ctx):
        await ctx.send("https://www.youtube.com/watch?v=0cfDlEN6uSE")
    
    @commands.command(name="lemon")
    async def _lemon(self, ctx):
        await ctx.send(":lemon:")

def setup(bot):
    bot.add_cog(Fun(bot))

#[                                                                                                                                ]