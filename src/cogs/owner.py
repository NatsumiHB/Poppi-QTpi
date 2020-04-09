from discord.ext import commands
from discord.ext.commands import dm_only, check, command
import discord
import config
import os


def is_owner():
    async def predicate(ctx):
        return ctx.author.id == config.owner_id
    return commands.check(predicate)


class Owner(commands.Cog, name="Owner"):
    def __init__(self, bot):
        self.bot = bot

    @command(help="Command to update from git")
    @dm_only()
    @is_owner()
    async def update(self, ctx):
        os.system("git -C ../ pull")

        user = self.bot.get_user(config.owner_id)
        embed = discord.Embed(description="Pulled from git!", color=discord.Color.green())
        await user.send(embed=embed, delete_after=5)

        os.execv("/app/src/main.py", [])
