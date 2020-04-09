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
