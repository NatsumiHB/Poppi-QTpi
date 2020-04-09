#!/usr/bin/python

from discord.ext import commands
import discord
import logging
import coloredlogs
from cogs.help_and_information import HelpAndInformation
from cogs.moderation import Moderation
from cogs.fun import Fun
import os
import sys

# Set up logging
coloredlogs.install(level="WARNING", fmt="[%(asctime)s][%(levelname)s]: %(message)s")
logging.getLogger("discord").addHandler(logging.FileHandler(filename="../poppi.log", encoding="utf-8", mode="w"))
logging.getLogger("discord").addHandler(logging.StreamHandler(sys.stdout))

bot = commands.Bot(command_prefix=os.getenv("PREFIX"), activity=discord.Game(name="poppi help"))


@bot.event
async def on_ready():
    owner_user = bot.get_user(bot.owner_id)
    logging.warning(f"{bot.user.name} running!\nOwner is {owner_user.display_name}!\nPrefix: '{os.getenv('PREFIX')}'")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("You are lacking permissions!")

    if isinstance(error, commands.BadArgument):
        return await ctx.send("Bad argument provided! (Consult help for usage information)")

    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send("Please provide all required arguments! (Consult help for usage information)")

    # Ignore errors
    else:
        return await ctx.send(error.message)


bot.remove_command("help")
bot.add_cog(HelpAndInformation(bot))
bot.add_cog(Moderation(bot))
bot.add_cog(Fun(bot))
bot.run(os.getenv("POPPI_TOKEN"))
