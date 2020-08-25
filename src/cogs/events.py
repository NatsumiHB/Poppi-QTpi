import logging

from discord.ext import commands

from poppi import error_embed, Poppi


class Events(commands.Cog):
    def __init__(self, bot: Poppi):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Update the help embed and commands JSON
        self.bot.update_help()

        # Log basic info
        logging.info(f"{self.bot.user.name} running!")
        logging.info(f"Default prefix is \"{self.bot.command_prefix}\"")
        logging.info(f"Currently {len(self.bot.commands)} commands "
                     f"in a total of {len(self.bot.cogs)} cogs are registered")
        logging.info(f"On {len(self.bot.guilds)} guilds "
                     f"with a total of {sum(len(g.members) for g in self.bot.guilds)} members")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
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

        if isinstance(error, commands.NSFWChannelRequired):
            return await ctx.send(embed=error_embed("This command only works in NSFW channels!"))

        if isinstance(error, commands.CommandNotFound):
            return logging.warning(f"Unknown command called: {ctx.message.content}")

        # Invoked command threw error
        if isinstance(error, commands.CommandInvokeError):
            logging.warning(error)
            try:
                return await ctx.send(embed=error_embed(error))
            except Exception as e:
                logging.warning(f"Tried sending error_embed in CommandInvokeError but couldn't: {e}")

        # Ignore errors
        else:
            return logging.warning(f"Error: {error}")
