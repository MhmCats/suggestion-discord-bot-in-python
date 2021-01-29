import discord
from discord.ext import commands

import asyncio
import random
import aiohttp
import praw

import datetime

reddit = praw.Reddit(client_id = '1wiwbWjgMVMdgg', 
                     client_secret = '1RDIac0bAfdw2LnefIIerEm4vXhKZw', 
                     user_agent = 'bot-memes-getter')
    
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="cat")
    async def _cat(self, ctx):
        async with aiohttp.ClientSession().get('https://api.thecatapi.com/v1/images/search') as resp:
            if resp.status != 200:
                embed = discord.Embed(color=discord.Colour.red(),
                                      description="Sorry we couldn't reach the cats...")
                embed.set_author(name="Error",
                                 icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
                await ctx.send(embed=embed)
                return await resp.close()
            js = await resp.json()
            embed = discord.Embed(title='Random Cat', color=discord.Colour.random())
            embed.set_image(url=js[0]['url'])
            await ctx.send(embed=embed)
            return await resp.close()
    
    @commands.command(name="dog")
    async def _dog(self, ctx):
        async with aiohttp.ClientSession().get('https://dog.ceo/api/breeds/image/random') as resp:
            if resp.status != 200:
                embed = discord.Embed(color=discord.Colour.red(),
                                      description="Sorry we couldn't reach the dogs...")
                embed.set_author(name="Error",
                                 icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
                await ctx.send(embed=embed)
                return await resp.close()
            js = await resp.json()
            embed = discord.Embed(title='Random Dog', color=discord.Colour.random())
            embed.set_image(url=js['message'])
            await ctx.send(embed=embed)
            return await resp.close()
    
    @commands.command(name="meme")
    async def _meme(self, ctx, *, subreddit = "memes"):
        top_submissions = []
        try:
            for submission in (reddit.subreddit(subreddit)).top(limit=100): 
                top_submissions.append(submission)
        except:
            embed = discord.Embed(color=discord.Colour.red(),
                                    description="Invalid Subreddit!!")
            embed.set_author(name="Error",
                                icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.send(embed=embed)
        choice = top_submissions[random.randint(1, 100)]
        embed = None; tries = 0
        while embed is None and tries < 5:
            if not choice.is_self and choice.url.endswith(".jpg"):
                embed = discord.Embed(color=discord.Colour.random(),
                                      description=f"**Posted by:** u/{choice.author}\n**Posted at:** {datetime.datetime.utcfromtimestamp(int(choice.created_utc)).strftime(('%d/%m/%Y at %H:%M'))}")
                embed.set_author(name=f"{choice.title}",
                                url=choice.url)
                embed.set_image(url=choice.url)
                embed.set_footer(text=f"Upvote Percentage: {int(choice.upvote_ratio*100)}% ({choice.score} upvotes in total)")
                return await ctx.send(embed=embed)
            else:
                choice = random.choice(top_submissions)
                tries += 1
                continue
        embed = discord.Embed(color=discord.Colour.red(),
                                    description="Could not find meme.")
        embed.set_author(name="Error",
                                icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))