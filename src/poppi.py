from datetime import datetime

import discord
from discord.ext import commands


class Poppi(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

        now = datetime.now()

        self.start_time = datetime.combine(now.date(), now.time())

    def get_uptime(self):
        now = datetime.now()
        duration = (datetime.combine(now.date(), now.time()) - self.start_time)
        seconds = duration.seconds

        # days, hours, minutes, seconds
        return duration.days, seconds // 3600, (seconds // 60) % 60, seconds

    def get_formatted_uptime(self, fmt):
        uptime = self.get_uptime()

        return fmt.format(uptime[0], uptime[1], uptime[2], uptime[3])


# Took this from R. Danny for simplicity
class FetchedUser(commands.Converter):
    async def convert(self, ctx, argument):
        if not argument.isdigit():
            raise commands.BadArgument('Not a valid user ID.')
        try:
            return await ctx.bot.fetch_user(argument)
        except discord.NotFound:
            raise commands.BadArgument('User not found.') from None
        except discord.HTTPException:
            raise commands.BadArgument('An error occurred while fetching the user.') from None


def success_embed(msg="Success!", color: discord.Color = discord.Color.green()):
    return discord.Embed(description=msg, color=color)


def error_embed(err="Error!", color: discord.Color = discord.Color.red()):
    return discord.Embed(description=err, color=color)
