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
                return await ctx.message.reply("You are blacklisted from suggestions!")
            else:
                continue

        if await self.check_suggestion_channel(ctx.message.guild) is None:
            return await ctx.message.reply("This guild has no suggestion channel to fix this either:\n > **1.** Make a channel called `#suggestions`\n > **2.**  Run the command `s!setup`")
        else:
            channel = await self.check_suggestion_channel(ctx.message.guild)
        
        if suggestion is None:
            return await ctx.message.reply("You did not provide a suggestion! To use this command run ```s!suggest <suggestion>```")
        
        if (len(suggestion) < 16):
            return await ctx.message.reply("You cannot possibly explain your suggestion in so few words - please try again!")
        
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
        
        if await self.check_suggestion_channel(ctx.message.guild) is None:
            return await ctx.message.reply("This guild has no suggestion channel to fix this either:\n > **1.** Make a channel called `#suggestions`\n > **2.**  Run the command `s!setup`")
        else:
            channel = await self.check_suggestion_channel(ctx.message.guild)
        
        if messageid is None:
            return await ctx.message.reply("You did not use this command correctly. The correct implementaton is ```s!editsuggestion [Message ID] <Reason>```")

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
        
        if await self.check_suggestion_channel(ctx.message.guild) is None:
            return await ctx.message.reply("This guild has no suggestion channel to fix this either:\n > **1.** Make a channel called `#suggestions`\n > **2.**  Run the command `s!setup`")
        else:
            channel = await self.check_suggestion_channel(ctx.message.guild)
        
        if messageid is None:
            return await ctx.message.reply("You did not use this command correctly. The correct implementaton is ```s!deletesuggestion [Message ID]```")

        message = await channel.fetch_message(messageid)

        webhook = await self.get_webhook(channel)
        if webhook is None:
            webhook = await channel.create_webhook(name="Suggestion Webhook")

        if str(ctx.message.author.id) in message.embeds[0].footer.text:
            await message.clear_reactions()
            async with aiohttp.ClientSession() as session:
                real_webhook = Webhook.from_url(webhook.url, adapter=AsyncWebhookAdapter(session))
                await real_webhook.edit_message(messageid, embed=None, content="This suggestion has been deleted.")
            
            emoji = "<:yes:802083268098785291>"
            await ctx.message.add_reaction(emoji)
        
        else:
            return await ctx.message.reply("That isn't your suggestion!")

    @commands.has_permissions(manage_guild=True)
    @commands.command(name="accept")
    async def _accept(self, ctx, messageid: int = None, *, reason = "No Reason"):
        
        if await self.check_suggestion_channel(ctx.message.guild) is None:
            return await ctx.message.reply("This guild has no suggestion channel to fix this either:\n > **1.** Make a channel called `#suggestions`\n > **2.**  Run the command `s!setup`")
        else:
            channel = await self.check_suggestion_channel(ctx.message.guild)

        if messageid is None:
            return await ctx.message.reply("You did not use this command correctly. The correct implementaton is ```s!accept [Message ID] <Reason>```")

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
            await ctx.message.reply("You are missing the permissions needed to use this command!", delete_after=3.0)
    
    @commands.has_permissions(manage_guild=True)
    @commands.command(name="deny")
    async def _deny(self, ctx, messageid: int = None, *, reason = "No Reason"):
        
        if await self.check_suggestion_channel(ctx.message.guild) is None:
            return await ctx.message.reply("This guild has no suggestion channel to fix this either:\n > **1.** Make a channel called `#suggestions`\n > **2.**  Run the command `s!setup`")
        else:
            channel = await self.check_suggestion_channel(ctx.message.guild)

        if messageid is None:
            return await ctx.message.reply("You did not use this command correctly. The correct implementaton is ```s!deny [Message ID] <Reason>```")

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
            await ctx.message.reply("You are missing the permissions needed to use this command!", delete_after=3.0)

    @commands.has_permissions(manage_guild=True)
    @commands.command(name="setup")
    async def _setup(self, ctx):
        for tchannel in ctx.guild.text_channels:
            if tchannel.name == "suggestions":
                return await ctx.message.reply("There is already a suggestion channel!")
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
        await channel.send("**__This is the new suggestion channel__**\n\nIf you type `s!suggest <Suggestion>` anywhere in this server it will pop up here! \n\nMembers who have **Manage Server** permissions can accept and deny suggestions. They can also blacklist people from suggestions. \n\nI hope you enjoy this bot!")

    @_setup.error 
    async def _setup_handler(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.reply("You are missing the permissions needed to use this command!", delete_after=3.0)

    @commands.has_permissions(manage_guild=True)
    @commands.command(name="blacklist")
    async def _blacklist(self, ctx, user: discord.Member = None):
        if user is None:
            return await ctx.message.reply("You did not use this command correctly. The correct implementation for that command is ```s!blacklist <Member>```")
        
        for role in user.roles:
            if role.name == "Suggestion Blacklist":
                return await ctx.message.reply("They are already blacklisted!")
        
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
            await ctx.message.reply("You are missing the permissions needed to use this command!", delete_after=3.0)

def setup(bot):
    bot.add_cog(Suggestions(bot))