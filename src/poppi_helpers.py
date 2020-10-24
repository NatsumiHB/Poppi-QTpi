import discord
from discord.ext import commands


class PoppiEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = discord.Color.purple()


# Simple error that can be used to easily throw errors
class PoppiError(commands.CommandError):
    def __init__(self, message: str):
        super().__init__(message)


# Took this from R. Danny (https://github.com/Rapptz/RoboDanny) for simplicity
class FetchedUser(commands.Converter):
    async def convert(self, ctx, argument):
        if not argument.isdigit():
            raise commands.BadArgument("Not a valid user ID")
        try:
            return await ctx.bot.fetch_user(argument)
        except discord.NotFound:
            raise commands.BadArgument("Couldn't find user") from None
        except discord.HTTPException:
            raise commands.BadArgument("An error occurred while fetching the user") from None


def success_embed(msg="Success!", color: discord.Color = discord.Color.green()):
    return discord.Embed(description=msg, color=color)


def error_embed(err="Error!", color: discord.Color = discord.Color.red()):
    return discord.Embed(description=str(err), color=color)  # Errors don't automatically get turned into an str
