import asyncio
import logging

from discord.ext import commands

from poppi import Poppi
from poppi_helpers import error_embed, PoppiError


class Events(commands.Cog):
    def __init__(self, bot: Poppi):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Update the help embed and commands JSON
        self.bot.update_help()

        # Update store embed
        self.bot.update_store()

        # Log basic info
        logging.info(f"{self.bot.user.name} running!")
        logging.info(f"Default prefix is \"{self.bot.command_prefix}\"")
        logging.info(f"Currently {len(self.bot.commands)} commands "
                     f"in a total of {len(self.bot.cogs)} cogs are registered")
        logging.info(f"On {len(self.bot.guilds)} guilds "
                     f"with a total of {sum(len(g.members) for g in self.bot.guilds)} members")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        error_message = "An unknown error occured!"

        if isinstance(error, commands.MissingPermissions):
            error_message = "You are lacking permissions!"

        if isinstance(error, commands.BotMissingPermissions):
            error_message = "I am lacking the permissions to do that!"

        if isinstance(error, commands.BadArgument) or isinstance(error, commands.BadUnionArgument):
            error_message = "Bad argument provided! (Consult help for usage information)"

        if isinstance(error, commands.MissingRequiredArgument):
            error_message = "Please provide all required arguments! (Consult help for usage information)"

        if isinstance(error, commands.NSFWChannelRequired):
            error_message = "This command only works in NSFW channels!"

        if isinstance(error, commands.CommandNotFound):
            error_message = f"Unknown command called: {ctx.message.content}"

        if isinstance(error, PoppiError):
            error_message = error

        if isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, asyncio.TimeoutError):
                error_message = "Command timed out!"

            logging.warning(error)

        # Everything else
        else:
            return logging.warning(f"Error: {error}")

        try:
            await ctx.send(embed=error_embed(error_message))
        except Exception as e:
            logging.warning(f"Tried sending error_embed but couldn't: {e}")
