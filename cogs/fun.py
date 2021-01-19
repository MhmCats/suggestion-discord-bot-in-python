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

        message = await ctx.send(f"```Hacking {user}...\n\n[                                                                                                                                ]\n\nETA: 11s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Grabbing Token... \n\n[##########                                                                                                                      ]\n\nETA: 10s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Downloading friends list \n\n[#######################                                                                                                         ]\n\nETA: 9s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Found most said word: {random.choice(words)} \n\n[################################                                                                                                ]\n\nETA: 8s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Calculating age \n\n[#############################################                                                                                   ]\n\nETA: 7s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Found age: {random.randint(13, 35)} \n\n[##########################################################                                                                      ]\n\nETA: 6s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Spamming in every server... \n\n[#########################################################################                                                       ]\n\nETA: 5s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Got banned for spamming in every server... \n\n[###################################################################################                                             ]\n\nETA: 4s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Unbanning myself \n\n[###############################################################################################                                 ]\n\nETA: 3s```")
        await asyncio.sleep(1) #11111111111
        await message.edit(content=f"```Favourite game: {random.choice(games)} \n\n[########################################################################################################                        ]\n\nETA: 2s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Spreading Trojan Viruses \n\n[####################################################################################################################            ]\n\nETA: 1s```")
        await asyncio.sleep(1)
        await message.edit(content=f"```Finished Hacking {user} \n\n[################################################################################################################################]\n\nETA: Done!```")


def setup(bot):
    bot.add_cog(Fun(bot))

#[                                                                                                                                ]