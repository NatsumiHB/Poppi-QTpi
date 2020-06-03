#!/usr/bin/python

import logging
import os

import coloredlogs
import discord
from discord.ext import commands

from cogs.TopGG import TopGG
from cogs.fun import Fun
from cogs.help_and_information import HelpAndInformation
from cogs.moderation import Moderation
from cogs.roles import Roles
from poppi import Poppi, error_embed

# Set up logging
coloredlogs.install(level="INFO", fmt="[%(asctime)s][%(levelname)s]: %(message)s")

bot = Poppi(command_prefix=os.getenv("POPPI_PREFIX"),
            activity=discord.Game(name="poppi help"),
            owner_id=os.getenv("POPPI_OWNER_ID"))


@bot.event
async def on_ready():
    logging.info(f"{bot.user.name} running!")
    logging.info(f"Prefix is '{os.getenv('POPPI_PREFIX')}'")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send(embed=error_embed("You are lacking permissions!"))

    if isinstance(error, commands.BotMissingPermissions):
        return await ctx.send(embed=error_embed("I am lacking the permissions to do that!"))

    if isinstance(error, commands.BadArgument):
        return await ctx.send(embed=error_embed("Bad argument provided! (Consult help for usage information)"))

    if isinstance(error, commands.BadUnionArgument):
        return await ctx.send(embed=error_embed("Bad (union) argument provided! (Consult help for usage information)"))

    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send(embed=error_embed("Please provide all required arguments! (Consult help for usage "
                                                "information)"))

    if isinstance(error, commands.CommandNotFound):
        return logging.warning(f"Unknown command called: {ctx.message.content}")

    # Invoked command threw error
    if isinstance(error, commands.CommandInvokeError):
        return await ctx.send(embed=error_embed(str(error)))

    # Ignore errors
    else:
        return logging.warning(f"Error: {type(error)}")


bot.remove_command("help")
bot.add_cog(HelpAndInformation(bot))
bot.add_cog(Moderation(bot))
bot.add_cog(Roles(bot))
bot.add_cog(Fun(bot))
bot.add_cog(TopGG(bot))
bot.run(os.getenv("POPPI_TOKEN"))
