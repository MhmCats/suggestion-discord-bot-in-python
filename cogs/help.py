import discord
from discord.ext import commands

import asyncio

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):
        
        menu = discord.Embed(color=discord.Colour.gold(),
                             description="This is the Help Menu for Suggestion Bot. Use the reactions to navigate.")
        menu.set_author(name="Help Menu 1/5",
                            icon_url=ctx.message.author.avatar_url)
        
        menu.add_field(name="Contents",
                       value="**1.** This page\n**2.** Suggestion Commands\n**3.** Utility commands\n**4.** Fun Commands\n**5.** Bot Owner/Admin Commands",
                       inline=False)
        menu.add_field(name="Reactions",
                       value="⏪ Go to the first page\n ◀️ Go backwards a page\n ⏹️ Delete the message\n ▶️ Go forward a page"
                             "\n ⏩ Go to the last page\n 🔢 Navigate to a page number",
                       inline=False)

        
        admin = discord.Embed(color=discord.Colour.gold(), 
                                description="Super secret admin commmands that only the bot owner can use!")
        admin.set_author(name="Help For Admin Commands 5/5",
                            icon_url=ctx.message.author.avatar_url)
        
        admin.add_field(name="Eval",
                        value="```s!eval <Code>```")
        admin.add_field(name="Load",
                        value="```s!load <Cog>```")
        admin.add_field(name="Unload",
                        value="```s!unload <Cog>```")
        admin.add_field(name="Reload",
                        value="```s!reload <Cog>```")
        
        suggestion = discord.Embed(color=discord.Colour.gold(),
                                description="Commands for the suggestion feature of the bot")
        suggestion.set_author(name="Help For Suggestion Commands 2/5",
                            icon_url=ctx.message.author.avatar_url)
        
        suggestion.add_field(name="Suggest",
                        value="```s!suggest <Suggestion>```",
                        inline=False)
        suggestion.add_field(name="Accept",
                        value=":warning: This command needs permissons of `Manage Server` to be executed ```s!accept <Message ID> [Reason]```",
                        inline=False)
        suggestion.add_field(name="Deny",
                        value=":warning: This command needs permissons of `Manage Server` to be executed ```s!deny <Message ID> [Reason]```",
                        inline=False)
        suggestion.add_field(name="Blacklist",
                        value=":warning: This command needs permissons of `Manage Server` to be executed ```s!blacklist <Member>```",
                        inline=False)
        suggestion.add_field(name="Setup",
                        value=":warning: This command needs permissons of `Manage Server` to be executed ```s!setup```",
                        inline=False)

        suggestion.set_footer(text="For the arguements, arguements that are surrounded in <> are required and [] are optional. You do not need these when executing a command.")

        fun = discord.Embed(color=discord.Colour.gold(),
                                description="Help for the fun commands of the bot")
        fun.set_author(name="Help For Fun Commands 4/5",
                            icon_url=ctx.message.author.avatar_url)
        
        fun.add_field(name="Hack",
                        value="```s!hack [Member]```",
                        inline=False)
        fun.add_field(name="Calmly",
                        value="```s!calmly```",
                        inline=False)
        fun.add_field(name="Lemon",
                        value="```s!lemon```",
                        inline=False)
        fun.set_footer(text="For the arguements, arguements that are surrounded in <> are required and [] are optional. You do not need these when executing a command.")

        utility = discord.Embed(color=discord.Colour.gold(),
                                description="Commands for the utility feature of the bot")
        utility.set_author(name="Help For Utility Commands 3/5",
                            icon_url=ctx.message.author.avatar_url)

        utility.add_field(name="Ping",
                        value="```s!ping```",
                        inline=False)
        utility.add_field(name="Calculate",
                        value="The operations that are supported are pythonian as well as a standalone sqrt() option ```s!calculate <Operation>```",
                        inline=False)
        utility.add_field(name="User Info",
                        value="```s!userinfo [User]```",
                        inline=False)
        utility.add_field(name="Links",
                        value="```s!links```",
                        inline=False)
        
        utility.set_footer(text="For the arguements, arguements that are surrounded in <> are required and [] are optional. You do not need these when executing a command.")

        embeds = {1: menu,
                  2: suggestion,
                  3: utility,
                  4: fun,
                  5: admin}
        
        message = await ctx.send(embed=menu)
        await message.add_reaction("⏪")
        await message.add_reaction("◀️")
        await message.add_reaction("⏹️")
        await message.add_reaction("▶️")
        await message.add_reaction("⏩")
        await message.add_reaction("🔢")
        page = 1 

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0)
                if user == ctx.author and str(reaction) in ["⏪", "◀️", "▶️", "⏩", "⏹️", "🔢"]:
                    if str(reaction.emoji) == "⏪" and page != 1:
                        page = 1
                        await message.edit(embed=embeds[page])
                    
                    elif str(reaction.emoji) == "◀️" and page != 1:
                        page -= 1
                        await message.edit(embed=embeds[page])
                    
                    elif str(reaction.emoji) == "▶️" and page != 5:
                        page += 1
                        await message.edit(embed=embeds[page])
                    
                    elif str(reaction.emoji) == "⏩" and page != 5:
                        page = 5
                        await message.edit(embed=embeds[page])

                    elif str(reaction.emoji) == "⏹️":
                        await message.delete()
                        return
                    
                    elif str(reaction.emoji) == "🔢":
                        number = None
                        question = await ctx.send("Which page do you wish to go to?")
                        while number is None:
                            try:
                                response = await self.bot.wait_for("message", timeout=60.0)
                                if response.author == ctx.author:
                                    try:
                                        number = int(response.content)
                                    except ValueError:
                                        number = None
                                        continue
                            except asyncio.TimeoutError:
                                return
                        await question.delete()
                        await response.delete()
                        page = number
                        await message.edit(embed=embeds[page])

                    await message.remove_reaction(str(reaction.emoji), ctx.author)
                else:
                    continue

            except asyncio.TimeoutError:
                return

def setup(bot):
    bot.add_cog(Help(bot))