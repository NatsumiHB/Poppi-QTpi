import logging

import discord
from discord.ext import commands

from poppi import error_embed


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Update the help embed and commands JSON
        self.bot.update_help()

        # Log basic info
        logging.info(f"{self.bot.user.name} running!")
        logging.info(f"Prefix is \"{self.bot.command_prefix}\"")
        logging.info(f"Currently {len(self.bot.commands)} commands in {len(self.bot.cogs)} cogs are registered")
        logging.info(f"On {len(self.bot.guilds)} guilds")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(embed=error_embed("You are lacking permissions!"))

        if isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(embed=error_embed("I am lacking the permissions to do that!"))

        if isinstance(error, commands.BadArgument):
            return await ctx.send(embed=error_embed("Bad argument provided! (Consult help for usage information)"))

        if isinstance(error, commands.BadUnionArgument):
            return await ctx.send(
                embed=error_embed("Bad (union) argument provided! (Consult help for usage information)")
            )

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(embed=error_embed("Please provide all required arguments! (Consult help for usage "
                                                    "information)"))

        if isinstance(error, commands.CommandNotFound):
            return logging.warning(f"Unknown command called: {ctx.message.content}")

        # Invoked command threw error
        if isinstance(error, commands.CommandInvokeError):
            logging.warning(str(error))
            try:
                return await ctx.send(embed=error_embed(str(error)))
            except Exception as e:
                logging.warning(f"Tried sending error_embed in CommandInvokeError but couldn't: {str(error)}")

        # Ignore errors
        else:
            return logging.warning(f"Error: {str(error)}")
