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
            activity=discord.Game(name=f"{os.getenv('POPPI_PREFIX')}help"),
            owner_id=os.getenv("POPPI_OWNER_ID"))


@bot.event
async def on_ready():
    # Update the help embed
    bot.update_help_embed()

    # Log basic info
    logging.info(f"{bot.user.name} running!")
    logging.info(f"Prefix is \"{bot.command_prefix}\"")
    logging.info(f"Currently {len(bot.commands)} commands in {len(bot.cogs)} cogs are registered")
    logging.info(f"On {len(bot.guilds)} guilds")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send(embed=error_embed("You are lacking permissions!"))

    if isinstance(error, commands.BotMissingPermissions):
        if error.missing_perms == discord.Permissions.send_messages:
            return logging.warning(f"Unknown command called: {ctx.message.content}")
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
        logging.warning(str(error))
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
