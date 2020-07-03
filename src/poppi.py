import os
import sqlite3

import discord
from discord.ext import commands


class PoppiEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = discord.Color.purple()


class Poppi(commands.Bot):
    def __init__(self, **options):
        self.default_prefix = os.getenv("POPPI_PREFIX")

        # Help embed for help command and commands_json for web API
        self.help_embed = None
        self.commands_json = None

        # Open DB and create table if it doesn't exist yet
        self.db_conn = sqlite3.connect("../bot_db.sqlite")
        self.db_cursor = self.db_conn.cursor()
        self.db_cursor.execute(r"CREATE TABLE IF NOT EXISTS prefixes (guild_id text PRIMARY KEY, prefix text NOT NULL)")

        super().__init__(command_prefix=self.get_prefix,
                         activity=discord.Game(name=f"{self.default_prefix}help"),
                         owner_id=os.getenv("POPPI_OWNER_ID"),
                         **options)

    async def get_prefix(self, message):
        if message.guild:
            custom_prefix = self.db_cursor.execute(
                "SELECT prefix FROM prefixes WHERE guild_id=?",
                (message.guild.id,)
            ).fetchone()

            if not custom_prefix:
                return [self.default_prefix]
            else:
                # Need to access the first element as fetchone returns a tuple
                return [self.default_prefix, custom_prefix[0]]
        else:
            return [self.default_prefix]

    # Updates the help embed and commands JSON to contain the most current cogs and commands
    def update_help(self):
        self.help_embed = PoppiEmbed(title=f"Help for {self.user.display_name}") \
            .set_thumbnail(url=self.user.avatar_url) \
            .set_footer(text=f"Running discord.py v.{discord.__version__} | '?' means argument is optional")

        # Get longest command name and usage info
        longest_cmd_len = len(max(
            (', '.join([bot_command.name] + bot_command.aliases) for bot_command in self.commands),
            key=len)
        )
        longest_usage_len = len(max((bot_command.usage for bot_command in self.commands), key=len))

        # Loop through all commands and cogs to generate help
        # Uses a generator in order to only return cogs with commands
        for cog in (cog for cog in self.cogs if cog not in ["TopGG", "Events"]):
            # Generate each help string
            bot_commands = "\n".join(f"`{', '.join([bot_command.name] + bot_command.aliases):<{longest_cmd_len}} "
                                     f"{bot_command.usage:<{longest_usage_len}}` -> "
                                     f"{bot_command.help}"
                                     for bot_command in self.get_cog(cog).get_commands())

            self.help_embed.add_field(name=cog, value=bot_commands, inline=False)

        # Set the commands_json for the web API
        self.commands_json = {
            cog: {command.name: command.help for command in self.get_cog(cog).get_commands()}
            for cog in self.cogs if cog not in ["TopGG", "Events"]
        }


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


# Negative reactions
def error_embed(err="Error!", color: discord.Color = discord.Color.red()):
    return discord.Embed(description=err, color=color)
