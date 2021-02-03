import discord
from discord.ext import commands

from discord import Webhook, AsyncWebhookAdapter
import aiohttp

import datetime

class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def check_suggestion_channel(self, guild):
        for channel in guild.text_channels:
            if "suggestions" in channel.name:
                return channel
            else:
                continue
        return None

    async def get_webhook(self, channel):
        webhooks = await channel.webhooks()
        try: 
            return webhooks[0]
        except IndexError:
            return None

    async def add_reaction(self, channel):    
        async for message in channel.history(limit=1):
            yes = "<:yes:802083268098785291>"
            no = "<:no:802083299559473222>"
            await message.add_reaction(yes)
            await message.add_reaction(no)

            return

    @commands.command(name="suggest")
    async def _suggest(self, ctx, *, suggestion: str = None):

        for role in ctx.message.author.roles:
            if role.name == "Suggestion Blacklist":
                embed = discord.Embed(color=discord.Colour.red(),
                                      description="You are blacklisted from suggestions!")
                embed.set_author(name="Error", 
                                 icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
                return await ctx.message.reply(embed=embed)
            else:
                continue

        if await self.check_suggestion_channel(ctx.message.guild) is None:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="This guild has no suggestion channel to fix this either:\n > **1.** Make a channel called `#suggestions`\n > **2.**  Run the command `s!setup`")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed)
        else:
            channel = await self.check_suggestion_channel(ctx.message.guild)
        
        if suggestion is None:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="You did not provide a suggestion! To use this command run ```s!suggest <suggestion>```")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed)
        
        if (len(suggestion) < 16):
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="You cannot possibly explain your suggestion in so few words - please try again!")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed)
        
        webhook = await self.get_webhook(channel)
        if webhook is None:
            webhook = await channel.create_webhook(name="Suggestion Webhook")
        
        embed = discord.Embed(color=discord.Colour.gold(),
                              description=f"**Suggestion:** {suggestion}")
        embed.set_footer(text=f"Open | {ctx.message.author.id}")
        embed.set_author(name=ctx.message.author,
                         icon_url=ctx.message.author.avatar_url)

        async with aiohttp.ClientSession() as session:
            real_webhook = Webhook.from_url(webhook.url, adapter=AsyncWebhookAdapter(session))
            await real_webhook.send(embed=embed,
                                    username=ctx.message.author.display_name,
                                    avatar_url=ctx.message.author.avatar_url,
                                    allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))
        
        await self.add_reaction(channel)
        
        emoji = "<:yes:802083268098785291>"
        await ctx.message.add_reaction(emoji)
    
    @commands.command(name="editsuggestion")
    async def _editsuggestion(self, ctx, messageid: int = None, *, newcontent = None):

        for role in ctx.message.author.roles:
            if role.name == "Suggestion Blacklist":
                embed = discord.Embed(color=discord.Colour.red(),
                                      description="You are blacklisted from suggestions!")
                embed.set_author(name="Error",
                                 icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
                return await ctx.message.reply(embed=embed)
            else:
                continue
        
        if await self.check_suggestion_channel(ctx.message.guild) is None:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="This guild has no suggestion channel to fix this either:\n > **1.** Make a channel called `#suggestions`\n > **2.**  Run the command `s!setup`")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed)
        else:
            channel = await self.check_suggestion_channel(ctx.message.guild)
        
        if messageid is None:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="You did not use this command correctly. The correct implementaton is ```s!editsuggestion [Message ID] <Reason>```")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed)

        message = await channel.fetch_message(messageid)

        webhook = await self.get_webhook(channel)
        if webhook is None:
            webhook = await channel.create_webhook(name="Suggestion Webhook")

        if str(ctx.message.author.id) in message.embeds[0].footer.text:
            
            embed = discord.Embed(color=discord.Colour.gold(),
                                description=f"**Suggestion:** {newcontent}")
            embed.set_footer(text=f"Open | {ctx.message.author.id}")
            embed.set_author(name=ctx.message.author,
                             icon_url=ctx.message.author.avatar_url)
            
            async with aiohttp.ClientSession() as session:
                real_webhook = Webhook.from_url(webhook.url, adapter=AsyncWebhookAdapter(session))
                await real_webhook.edit_message(messageid, embed=embed)
            
            emoji = "<:yes:802083268098785291>"
            await ctx.message.add_reaction(emoji)
        
        else:
            return await ctx.message.reply("That isn't your suggestion!")
    
    @commands.command(name="deletesuggestion")
    async def _deletesuggestion(self, ctx, messageid: int = None):

        for role in ctx.message.author.roles:
            if role.name == "Suggestion Blacklist":
                embed = discord.Embed(color=discord.Colour.red(),
                                      description="You are blacklisted from suggestions!")
                embed.set_author(name="Error",
                                 icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
                return await ctx.message.reply(embed=embed)
            else:
                continue
        
        if await self.check_suggestion_channel(ctx.message.guild) is None:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="This guild has no suggestion channel to fix this either:\n > **1.** Make a channel called `#suggestions`\n > **2.**  Run the command `s!setup`")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed)
        else:
            channel = await self.check_suggestion_channel(ctx.message.guild)
        
        if messageid is None:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="You did not use this command correctly. The correct implementaton is ```s!deletesuggestion <Message ID>```")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed)

        message = await channel.fetch_message(messageid)

        webhook = await self.get_webhook(channel)
        if webhook is None:
            webhook = await channel.create_webhook(name="Suggestion Webhook")

        if str(ctx.message.author.id) in message.embeds[0].footer.text:
            
            async with aiohttp.ClientSession() as session:
                real_webhook = Webhook.from_url(webhook.url, adapter=AsyncWebhookAdapter(session))
                await real_webhook.edit_message(messageid, embed=None, content="This suggestion has been deleted.")
            
            emoji = "<:yes:802083268098785291>"
            await ctx.message.add_reaction(emoji)
        
        else:
            return await ctx.message.reply("That isn't your suggestion!")

    @commands.has_permissions(manage_guild=True)
    @commands.command(name="consider")
    async def _consider(self, ctx, messageid: int = None):
        
        if await self.check_suggestion_channel(ctx.message.guild) is None:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="This guild has no suggestion channel to fix this either:\n > **1.** Make a channel called `#suggestions`\n > **2.**  Run the command `s!setup`")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed)
        else:
            channel = await self.check_suggestion_channel(ctx.message.guild)

        if messageid is None:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="You did not use this command correctly. The correct implementaton is ```s!consider <Message ID>```")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed)

        message = await channel.fetch_message(messageid)
                
        webhook = await self.get_webhook(channel)
        if webhook is None:
            webhook = await channel.create_webhook(name="Suggestion Webhook")
        if "Open" in message.embeds[0].footer.text:
            await message.clear_reactions()
            
            embed = discord.Embed(color=discord.Colour.orange(),
                                  title="Suggestion under consideration",
                                description=f"{message.embeds[0].description}")
            embed.set_footer(text=f"Open")
            embed.set_author(name=message.embeds[0].author.name,
                            icon_url=message.embeds[0].author.icon_url)
            
            async with aiohttp.ClientSession() as session:
                real_webhook = Webhook.from_url(webhook.url, adapter=AsyncWebhookAdapter(session))
                await real_webhook.edit_message(messageid, embed=embed)
            
            
            emoji = "<:yes:802083268098785291>"
            await ctx.message.add_reaction(emoji)
        else:
            return await ctx.message.reply("This suggestion has already been accepted/denied")
    
    
    @commands.has_permissions(manage_guild=True)
    @commands.command(name="accept")
    async def _accept(self, ctx, messageid: int = None, *, reason = "No Reason"):
        
        if await self.check_suggestion_channel(ctx.message.guild) is None:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="This guild has no suggestion channel to fix this either:\n > **1.** Make a channel called `#suggestions`\n > **2.**  Run the command `s!setup`")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed)
        else:
            channel = await self.check_suggestion_channel(ctx.message.guild)

        if messageid is None:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="You did not use this command correctly. The correct implementaton is ```s!accept <Message ID> [Reason]```")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed)

        message = await channel.fetch_message(messageid)
                
        webhook = await self.get_webhook(channel)
        if webhook is None:
            webhook = await channel.create_webhook(name="Suggestion Webhook")
        if "Open" in message.embeds[0].footer.text:
            await message.clear_reactions()
            
            embed = discord.Embed(color=discord.Colour.green(),
                                description=f"{message.embeds[0].description}\n\n**Accepted by {ctx.message.author}:** {reason}")
            embed.set_footer(text=f"Closed")
            embed.set_author(name=message.embeds[0].author.name,
                            icon_url=message.embeds[0].author.icon_url)
            
            async with aiohttp.ClientSession() as session:
                real_webhook = Webhook.from_url(webhook.url, adapter=AsyncWebhookAdapter(session))
                await real_webhook.edit_message(messageid, embed=embed)
            
            
            emoji = "<:yes:802083268098785291>"
            await ctx.message.add_reaction(emoji)
        else:
            return await ctx.message.reply("This suggestion has already been accepted/denied")
    
    @_accept.error 
    async def _accept_handler(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="You are missing the permissions needed to use this command!")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed, delete_after=5.0)
    
    @commands.has_permissions(manage_guild=True)
    @commands.command(name="deny")
    async def _deny(self, ctx, messageid: int = None, *, reason = "No Reason"):
        
        if await self.check_suggestion_channel(ctx.message.guild) is None:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="This guild has no suggestion channel to fix this either:\n > **1.** Make a channel called `#suggestions`\n > **2.**  Run the command `s!setup`")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed)
        else:
            channel = await self.check_suggestion_channel(ctx.message.guild)

        if messageid is None:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="You did not use this command correctly. The correct implementaton is ```s!deny [Message ID] <Reason>```")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed)

        message = await channel.fetch_message(messageid)
        
        webhook = await self.get_webhook(channel)
        if webhook is None:
            webhook = await channel.create_webhook(name="Suggestion Webhook")
        if "Open" in message.embeds[0].footer.text:

            await message.clear_reactions()
                
            embed = discord.Embed(color=discord.Colour.red(),
                                description=f"{message.embeds[0].description}\n\n**Denied by {ctx.message.author}:** {reason}")
            embed.set_footer(text=f"Closed")
            embed.set_author(name=message.embeds[0].author.name,
                            icon_url=message.embeds[0].author.icon_url)
            
            async with aiohttp.ClientSession() as session:
                real_webhook = Webhook.from_url(webhook.url, adapter=AsyncWebhookAdapter(session))
                await real_webhook.edit_message(messageid, embed=embed)

            emoji = "<:yes:802083268098785291>"
            await ctx.message.add_reaction(emoji)
        else:
            return await ctx.message.reply("This suggestion has already been accepted/denied")
    
    @_deny.error 
    async def _deny_handler(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="You are missing the permissions needed to use this command!")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed, delete_after=5.0)

    @commands.has_permissions(manage_guild=True)
    @commands.command(name="setup")
    async def _setup(self, ctx):
        for tchannel in ctx.guild.text_channels:
            if "suggestions" in tchannel.name:
                embed = discord.Embed(color=discord.Colour.red(),
                                  description="There is already a suggestion channel!")
                embed.set_author(name="Error",
                                 icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
                return await ctx.message.reply(embed=embed)
            else:
                continue
        
        channel = await ctx.guild.create_text_channel(name="suggestions", 
                                            topic="Type s!suggest <suggestion> in any channel and it will pop up here!",
                                            reason=f"Because {ctx.message.author} ran the command s!setup",
                                            category=ctx.message.channel.category,
                                            overwrites=ctx.message.channel.category.overwrites)
        await channel.create_webhook(name="Suggestion Webhook")
        
        emoji = "<:yes:802083268098785291>"
        await ctx.message.add_reaction(emoji)
        embed = discord.Embed(color=discord.Colour.gold(),
                              description="**__This is the new suggestion channel__**\n\nIf you type `s!suggest <Suggestion>` anywhere in this server it will pop up here! \n\nMembers who have **Manage Server** permissions can accept and deny suggestions. They can also blacklist people from suggestions. \n\nI hope you enjoy this bot!")
        embed.set_author(name="New Suggestion Channel",
                         icon_url="https://cdn.discordapp.com/avatars/743435729085923379/a1a5d77e6413466d58f95691eb290b6e.webp?size=128")
        return await channel.send(embed=embed)

    @_setup.error 
    async def _setup_handler(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="You are missing the permissions needed to use this command!")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed, delete_after=5.0)

    @commands.has_permissions(manage_guild=True)
    @commands.command(name="blacklist")
    async def _blacklist(self, ctx, user: discord.Member = None):
        if user is None:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="You did not use this command correctly. The correct implementation for that command is ```s!blacklist <Member>```")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed)
        
        for role in user.roles:
            if role.name == "Suggestion Blacklist":
                embed = discord.Embed(color=discord.Colour.red(),
                                      description="You did not use this command correctly. The correct implementation for that command is ```s!blacklist <Member>```")
                embed.set_author(name="Error",
                                 icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
                return await ctx.message.reply(embed=embed)
        
        for role in ctx.guild.roles:
            if role.name == "Suggestion Blacklist":
                blacklist_role = role
                break
        
        await user.add_roles(blacklist_role)
        
        emoji = "<:yes:802083268098785291>"
        await ctx.message.add_reaction(emoji)
        
    @_blacklist.error 
    async def _blacklist_handler(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="You are missing the permissions needed to use this command!")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.message.reply(embed=embed, delete_after=5.0)

def setup(bot):
    bot.add_cog(Suggestions(bot))