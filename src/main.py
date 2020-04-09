#!/usr/bin/python

from discord.ext import commands
import discord
import logging
import coloredlogs
from cogs.help_and_information import HelpAndInformation
from cogs.moderation import Moderation
from cogs.fun import Fun
import os

# Set up logging
coloredlogs.install(level="WARNING", fmt="[%(asctime)s][%(levelname)s]: %(message)s")

bot = commands.Bot(command_prefix=os.getenv("PREFIX"), activity=discord.Game(name="poppi help"))


@bot.event
async def on_ready():
    logging.warning(f"{bot.user.name} running!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("You are lacking permissions!")

    if isinstance(error, commands.BadArgument):
        return await ctx.send("Bad argument provided! (Consult help for usage information)")

    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send("Please provide all required arguments! (Consult help for usage information)")

    else:
        print(error)


bot.remove_command("help")
bot.add_cog(HelpAndInformation(bot))
bot.add_cog(Moderation(bot))
bot.add_cog(Fun(bot))
bot.run(os.getenv("POPPI_TOKEN"))
