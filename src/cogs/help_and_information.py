from discord.ext import commands
from discord.ext.commands import command
import discord
import os
from fetched_user import FetchedUser


class HelpAndInformation(commands.Cog, name="Help and Information"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @command(help="Display this")
    async def help(self, ctx):
        embed = discord.Embed(title=f"Help for {self.bot.user.display_name}", color=discord.Color.purple())
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        # Loop through all commands and cogs to generate help
        for cog in self.bot.cogs:
            if cog != "TopGG":
                commands = ""
                for command in self.bot.get_cog(cog).get_commands():
                    commands += f"{command.name} -> {command.help}\n"

                embed.add_field(name=cog, value=commands, inline=False)

        embed.set_footer(text=f"{self.bot.user.display_name} | Version {os.getenv('POPPI_VERSION')}")

        await ctx.send(embed=embed)

    @command(help="Get someone's avatar", usage="[mention|None]")
    async def avatar(self, ctx, user: FetchedUser = None):
        # Return avatar of author if no user is given
        if user is None:
            user = ctx.author

        embed = discord.Embed(color=discord.Color.purple())
        embed.set_author(name=f"{user.display_name}'s avatar", url=str(user.avatar_url))
        embed.set_image(url=user.avatar_url)

        await ctx.send(embed=embed)

    # @command(help="Information about me")
    # async def info(self, ctx):
    #     embed = discord.Embed(color=discord.Color.purple(), description=f"I'm on {len(self.bot.guilds)} servers!\n"
    #                                                                     f"Commit {os.getenv('POPPI_COMMIT')}")
    #     embed.set_author(name=f"Information about {self.bot.user.display_name}", icon_url=self.bot.user.avatar_url)
    #
    #     await ctx.send(embed=embed)

    @command(help="Send a support DM to my creator")
    async def support(self, ctx, *, msg):
        user = await self.bot.fetch_user(self.bot.owner_id)
        await user.send(f"Support request from {ctx.author.name}#{ctx.author.discriminator}:\n\n{msg}")
        embed = discord.Embed(description="Success!", color=discord.Color.green())

        await ctx.send(embed=embed)
