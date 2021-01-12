import platform

import discord
from discord.ext import commands
from pyArango.connection import Connection
from pyArango.theExceptions import CreationError

from api_helpers import APIUtils
from config import Config
from poppi_helpers import PoppiEmbed
from profile_helpers import ProfileHelpers


class Poppi(commands.Bot):
    def __init__(self, **options):
        # Set API Utils class
        self.api_utils = APIUtils()

        # Help embed for help command and commands_json for web API
        self.help_embeds = []
        self.commands_json = None
        self.store_embed = None

        # Create config
        self.config = Config()

        # Database stuff for the profile system
        conn = Connection(
            username="root",
            password=self.config.config["db_password"],
            arangoURL=f"http://{self.config.config['db_hostname']}:8529"
        )
        try:
            self.db = conn.createDatabase(name="poppi")
        except CreationError:
            self.db = conn["poppi"]

        try:
            self.profiles = self.db.createCollection(name="profiles")
        except CreationError:
            self.profiles = self.db["profiles"]

        try:
            self.store_items = self.db.createCollection(name="store_items")

            self.load_store()
        except CreationError:
            self.store_items = self.db["store_items"]

        # DB Helpers
        self.profile_helpers = ProfileHelpers(self.profiles, self.store_items, self.config)

        super().__init__(command_prefix=self.config.config["prefix"],
                         activity=discord.Game(name=f"{self.config.config['prefix']}help"),
                         owner_id=self.config.config["owner_id"],
                         **options)

    def load_store(self):
        for i, item in enumerate(self.config.config["base_store_items"]):
            store_item = self.store_items.createDocument()

            store_item.set({
                "id": i + 1,
                **item
            })

            store_item.save()

    async def reload_config(self):
        self.config = Config()

        await self.profile_helpers.client_session.close()

        self.profile_helpers = ProfileHelpers(self.profiles, self.store_items, self.config)

    # Updates the help embed and commands JSON to contain the most current cogs and commands
    def update_help(self):
        # Loop through all commands and cogs to generate help
        # Uses a generator in order to only return cogs with commands
        blacklist = ["Owner"]
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
            if len(self.get_cog(cog_name).get_commands()) > 0 and cog_name not in blacklist
        }

    def update_store_embed(self):
        longest_id_len = len(max(
            (str(item["id"])
             for item
             in self.store_items.fetchAll()),
            key=len)
        )
        longest_name_len = len(max(
            (str(item["name"])
             for item
             in self.store_items.fetchAll()),
            key=len)
        )

        self.store_embed = PoppiEmbed() \
            .add_field(name="Money",
                       value="\n".join(f"`{item['id']:<{longest_id_len}}: {item['name']:{longest_name_len}}` "
                                       f"({item['emoji']})"
                                       for item
                                       in self.store_items.fetchAll()),
                       inline=False)
