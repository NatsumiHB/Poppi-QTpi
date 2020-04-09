from discord.ext import commands
from discord.ext.commands import command
import discord
import os


class HelpAndInformation(commands.Cog, name="Help and Information"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @command(help="Get someone's avatar", usage="[mention]")
    async def avatar(self, ctx, user: discord.User):
        embed = discord.Embed(color=discord.Color.purple())
        embed.set_author(name=f"{user.display_name}'s avatar", url=str(user.avatar_url))
        embed.set_image(url=user.avatar_url)

        await ctx.send(embed=embed)

    @command(help="Information about me", usage="")
    async def info(self, ctx):
        embed = discord.Embed(color=discord.Color.purple(), description=f"I'm on {len(self.bot.guilds)} servers!")
        embed.set_author(name=f"Information about {self.bot.user.display_name}", icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=f"Version {os.getenv('VERSION')}")

        await ctx.send(embed=embed)

    @command(help="Send a support DM to my creator", usage="[msg]")
    async def support(self, ctx, *, msg):
        user = self.bot.get_user(self.bot.owner_id)
        await user.send(f"Support request from {ctx.author.display_name}#{ctx.author.discriminator}:\n\n```{msg}```")
        embed = discord.Embed(description="Success!", color=discord.Color.green())

        await ctx.send(embed=embed)
