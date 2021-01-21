import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="help", invoke_without_command=True)
    async def help(self, ctx, module = None):
        if module is None:
            embed = discord.Embed(color=discord.Colour.gold(),
                                  description="Type `s!help [Module Name]` for more information on modules.")
            embed.set_author(name="Help Menu",
                             icon_url=ctx.message.author.avatar_url)
            
            embed.add_field(name=":speech_balloon: Suggestion Commands :speech_balloon:",
                            value="```s!help suggestion```")
            embed.add_field(name=":lollipop: Fun Commands :lollipop:",
                            value="```s!help fun```")
            embed.add_field(name=":gear: Utility Commands :gear:",
                            value="```s!help utility```")
            
            if ctx.message.author.id == 737928480389333004:
                embed.add_field(name=":warning: Admin Commands :warning:",
                                value="```s!help admin```")
            
            await ctx.message.add_reaction('\u2705')
            await ctx.message.author.send(embed=embed)
        
        elif module == "admin":
        
            if not ctx.message.author.id == 737928480389333004:
                return
        
            embed = discord.Embed(color=discord.Colour.red(), 
                                  description="Super secret admin commmands that only the bot owner can use!")
            embed.set_author(name="Help For Admin Commands",
                             icon_url=ctx.message.author.avatar_url)
            
            embed.add_field(name="Eval",
                            value="```s!eval <Code>```")
            embed.add_field(name="Load",
                            value="```s!load <Cog>```")
            embed.add_field(name="Unload",
                            value="```s!unload <Cog>```")
            embed.add_field(name="Reload",
                            value="```s!reload <Cog>```")
            
            await ctx.message.add_reaction('\u2705')
            await ctx.message.author.send(embed=embed)
        
        elif module == "suggestion":
        
            embed = discord.Embed(color=discord.Colour.gold(),
                                  description="Commands for the suggestion feature of the bot")
            embed.set_author(name="Help For Suggestion Commands",
                             icon_url=ctx.message.author.avatar_url)
            
            embed.add_field(name="Suggest",
                            value="```s!suggest <Suggestion>```",
                            inline=False)
            embed.add_field(name="Accept",
                            value=":warning: This command needs permissons of `Manage Server` to be executed ```s!accept <Message ID> [Reason]```",
                            inline=False)
            embed.add_field(name="Deny",
                            value=":warning: This command needs permissons of `Manage Server` to be executed ```s!deny <Message ID> [Reason]```",
                            inline=False)
            embed.add_field(name="Blacklist",
                            value=":warning: This command needs permissons of `Manage Server` to be executed ```s!blacklist <Member>```",
                            inline=False)
            embed.add_field(name="Setup",
                            value=":warning: This command needs permissons of `Manage Server` to be executed ```s!setup```",
                            inline=False)

            embed.set_footer(text="For the arguements, arguements that are surrounded in <> are required and [] are optional. You do not need these when executing a command.")

            await ctx.message.add_reaction('\u2705') 
            await ctx.message.author.send(embed=embed)
        
        elif module == "fun":

            embed = discord.Embed(color=discord.Colour.gold(),
                                  description="Help for the fun commands of the bot")
            embed.set_author(name="Help For Fun Commands",
                             icon_url=ctx.message.author.avatar_url)
            
            embed.add_field(name="Hack",
                            value="```s!hack [Member]```",
                            inline=False)
            embed.add_field(name="Calmly",
                            value="```s!calmly```",
                            inline=False)
            embed.add_field(name="Lemon",
                            value="```s!lemon```",
                            inline=False)
            embed.set_footer(text="For the arguements, arguements that are surrounded in <> are required and [] are optional. You do not need these when executing a command.")

            await ctx.message.add_reaction('\u2705') 
            await ctx.message.author.send(embed=embed)
        
        elif module == "utility":
            
            embed = discord.Embed(color=discord.Colour.gold(),
                                  description="Commands for the utility feature of the bot")
            embed.set_author(name="Help For Utility Commands",
                             icon_url=ctx.message.author.avatar_url)

            embed.add_field(name="Ping",
                            value="```s!ping```",
                            inline=False)
            embed.add_field(name="Calculate",
                            value="The operations that are supported are pythonian as well as a standalone sqrt() option ```s!calculate <Operation>```",
                            inline=False)
            
            embed.set_footer(text="For the arguements, arguements that are surrounded in <> are required and [] are optional. You do not need these when executing a command.")

            await ctx.message.add_reaction('\u2705') 

            await ctx.message.author.send(embed=embed)

        else:
            await ctx.message.author.send("Module not found. Please try again.")

def setup(bot):
    bot.add_cog(Help(bot))