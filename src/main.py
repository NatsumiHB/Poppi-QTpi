from discord.ext import commands
import discord
import logging
import config
import coloredlogs
from cogs.help_and_information import HelpAndInformation
from cogs.moderation import Moderation
from cogs.fun import Fun

# Set up logging
coloredlogs.install(level="WARNING", fmt="[%(asctime)s][%(levelname)s]: %(message)s")

bot = commands.Bot(command_prefix=config.prefix)


@bot.event
async def on_ready():
    logging.warning(f"{bot.user.name} running!")

    await bot.change_presence(activity=discord.Game(name="poppi help"))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("You are lacking permissions!")

    if isinstance(error, commands.BadArgument):
        return await ctx.send("Bad argument provided! (Consult help for usage information)")

    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send("Please provide all required arguments! (Consult help for usage information)")


bot.remove_command("help")
bot.add_cog(HelpAndInformation(bot))
bot.add_cog(Moderation(bot))
bot.add_cog(Fun(bot))
bot.run(config.token)
