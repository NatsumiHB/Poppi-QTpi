from discord.ext import commands
from discord.ext.commands import command
import discord
import config


class HelpAndInformation(commands.Cog, name="Help and Information"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @command(help="Display this")
    async def help(self, ctx):
        embed = discord.Embed(title=f"Help for {self.bot.user.display_name}", color=discord.Color.purple())
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        for cog in self.bot.cogs:
            commands = ""
            for command in self.bot.get_cog(cog).get_commands():
                commands += f"{command.name} -> {command.help}\n"

            embed.add_field(name=cog, value=commands, inline=False)

        embed.set_footer(text=f"{self.bot.user.display_name} | Ping: {round(self.bot.latency, 1)}ms")

        await ctx.send(embed=embed)

    @command(help="Information about me")
    async def info(self, ctx):
        embed = discord.Embed(color=discord.Color.purple(), description=f"I'm on {len(self.bot.guilds)} servers!")
        embed.set_author(name=f"Information about {self.bot.user.display_name}", icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=f"Version {config.version}")
        await ctx.send(embed=embed)

    @command(help="Send a support DM to my creator")
    async def support(self, ctx, *, msg):
        user = self.bot.get_user(config.owner_id)
        await user.send(f"Support request from {ctx.author.display_name}#{ctx.author.discriminator}:\n\n```{msg}```")

    @command(help="Get someone's avatar")
    async def avatar(self, ctx, user: discord.User):
        embed = discord.Embed(title=f"{user.display_name}'s avatar", color=discord.Color.purple())
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)
