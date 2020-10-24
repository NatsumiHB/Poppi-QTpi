import json
import platform

import discord
from discord.ext import commands
from pyArango.connection import Connection
from pyArango.theExceptions import CreationError

from api_utils import APIUtils
from poppi_helpers import PoppiEmbed
from profile_helpers import ProfileHelpers


class Poppi(commands.Bot):
    def __init__(self, **options):
        # Set API Utils class
        self.api_utils = APIUtils()

        # Help embed for help command and commands_json for web API
        self.help_embeds = []
        self.commands_json = None

        # Load config
        with open("../config.json", "r") as config:
            self.config = json.loads(config.read())

        # Database stuff for the profile system
        conn = Connection(
            username="root",
            password=self.config["db_password"],
            arangoURL=f"http://{self.config['db_hostname']}:8529"
        )
        try:
            db = conn.createDatabase(name="poppi")
        except CreationError:
            db = conn["poppi"]

        try:
            profiles = db.createCollection(name="profiles")
        except CreationError:
            profiles = db["profiles"]

        # DB Helpers
        self.profile_helpers = ProfileHelpers(profiles, self.config)

        super().__init__(command_prefix=self.config["prefix"],
                         activity=discord.Game(name=f"{self.config['prefix']}help"),
                         owner_id=self.config["owner_id"],
                         **options)

    # Updates the help embed and commands JSON to contain the most current cogs and commands
    def update_help(self):
        # Loop through all commands and cogs to generate help
        # Uses a generator in order to only return cogs with commands
        blacklist = []
        for cog_name in (cog
                         for cog
                         in self.cogs
                         if len(self.get_cog(cog).get_commands()) > 0 and cog not in blacklist):
            cog = self.get_cog(cog_name)

            # Get longest command name and usage info (_sub is used for subcommands)
            longest_cmd_len = len(max(
                (', '.join([command.name, *command.aliases])
                 for command
                 in cog.walk_commands()),
                key=len)
            )
            longest_cmd_len_sub = len(max(
                (f"{f'{command.parent.name} ' if command.parent is not None else ''}"
                 f"{', '.join([command.name, *command.aliases])}"
                 for command
                 in cog.walk_commands()),
                key=len)
            )
            longest_usage_len = len(max((command.usage
                                         for command
                                         in cog.walk_commands()), key=len))

            # Only wrote this helper to not get over the max line-length according to PEP-8
            def cmd_len(command):
                return longest_cmd_len if command.parent is not None else longest_cmd_len_sub

            # Generate help embed
            cog_help = PoppiEmbed(title=f"Help for {self.user.display_name}") \
                .set_thumbnail(url=self.user.avatar_url) \
                .add_field(
                name=cog_name,
                value="\n".join(f"`{f'{command.parent.name} ' if command.parent is not None else ''}"
                                f"{', '.join([command.name, *command.aliases]):<{cmd_len(command)}} "
                                f"{command.usage:<{longest_usage_len}}` -> "
                                f"{command.help}"
                                for command
                                in cog.walk_commands()),
                inline=False) \
                .set_footer(text=f"Running discord.py {discord.__version__} | Python {platform.python_version()}")

            self.help_embeds.append(cog_help)

        # Set the commands_json for the web API
        self.commands_json = {
            cog_name: {f"{f'{command.parent.name} ' if command.parent is not None else ''}{command.name}": command.help
                       for command
                       in self.get_cog(cog_name).walk_commands()}
            for cog_name
            in self.cogs
            if len(self.get_cog(cog_name).get_commands()) > 0 and cog not in blacklist
        }
