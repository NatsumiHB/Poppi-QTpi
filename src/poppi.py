import datetime

import discord
from discord.ext import commands


class Poppi(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

        now = datetime.datetime.now()
        self.start_time = datetime.datetime.combine(now.date(), now.time())

        self.help_embed = None
        self.commands_json = None

    # Updates the help embed and commands JSON to contain the most current cogs and commands
    def update_help(self):
        self.help_embed = discord.Embed(title=f"Help for {self.user.display_name}", color=discord.Color.purple()) \
            .set_thumbnail(url=self.user.avatar_url)

        # Get longest command name and usage info
        longest_cmd_len = len(max((bot_command.name for bot_command in self.commands), key=len))
        longest_usage_len = len(max((bot_command.usage for bot_command in self.commands), key=len))

        # Loop through all commands and cogs to generate help
        # Uses a generator in order to only return cogs that aren't the TopGG cog
        for cog in (cog for cog in self.cogs if cog != "TopGG" and cog != "Events"):
            # Generate each help string
            bot_commands = "\n".join(f"`{bot_command.name:<{longest_cmd_len}} "
                                     f"{bot_command.usage:<{longest_usage_len}}` -> "
                                     f"{bot_command.help}"
                                     for bot_command in self.get_cog(cog).get_commands())

            self.help_embed.add_field(name=cog, value=bot_commands, inline=False)

        # Set the commands_json for the web API
        self.commands_json = {
            cog: {command.name: command.help for command in self.get_cog(cog).get_commands()}
            for cog in self.cogs if cog != "TopGG" and cog != "Events"
        }

    def get_uptime(self):
        now = datetime.datetime.now()
        seconds = (datetime.datetime.combine(now.date(), now.time()) - self.start_time).seconds

        # "dd days, hh:mm:ss"
        return str(datetime.timedelta(seconds=seconds))


# Took this from R. Danny (https://github.com/Rapptz/RoboDanny) for simplicity
class FetchedUser(commands.Converter):
    async def convert(self, ctx, argument):
        if not argument.isdigit():
            raise commands.BadArgument("Not a valid user ID.")
        try:
            return await ctx.bot.fetch_user(argument)
        except discord.NotFound:
            raise commands.BadArgument("User not found.") from None
        except discord.HTTPException:
            raise commands.BadArgument("An error occurred while fetching the user.") from None


# Positive reactions
def success_embed(msg="Success!", color: discord.Color = discord.Color.green()):
    return discord.Embed(description=msg, color=color)


async def thumbs_up_react(ctx: commands.Context):
    await ctx.message.add_reaction(":thumbs_up:")


# Negative reactions
def error_embed(err="Error!", color: discord.Color = discord.Color.red()):
    return discord.Embed(description=err, color=color)


async def thumbs_down_react(ctx: commands.Context):
    await ctx.message.add_reaction(":thumbs_down:")
