from typing import Union

import discord
from discord.ext import commands
from discord.ext.commands import command, guild_only

from poppi import success_embed, FetchedUser, Poppi, PoppiEmbed


class HelpAndInformation(commands.Cog, name="Help and Information"):
    def __init__(self, bot: Poppi):
        self.bot = bot

    @command(help="Display the help", usage="")
    async def help(self, ctx: commands.Context):
        # Send the bot's help embed which is defined by update_help_embed() in /src/poppi.py
        await ctx.send(embed=self.bot.help_embed)

    @command(help="Change the local prefix", usage="[string]")
    @guild_only()
    async def prefix(self, ctx: commands.Context, prefix: str = None):
        prefix = prefix if prefix is not None else self.bot.default_prefix

        self.bot.db_cursor.execute(
            "INSERT INTO prefixes (guild_id, prefix) VALUES (?, ?) ON CONFLICT(guild_id) DO UPDATE SET prefix=?",
            (ctx.guild.id, prefix, prefix,)
        )
        self.bot.db_conn.commit()

        await ctx.send(embed=success_embed(f"Updated prefix to `{prefix}`"))

    @command(help="Get someone's avatar", usage="[user|None]")
    async def avatar(self, ctx: commands.Context, user: Union[discord.User, FetchedUser] = None):
        # Return avatar of author if no user is given
        if user is None:
            user = ctx.author

        await ctx.send(embed=PoppiEmbed()
                       .set_author(name=f"{user.display_name}'s avatar", url=user.avatar_url)
                       .set_image(url=user.avatar_url))

    @command(help="Make an emoji bigger", usage="[emoji]")
    async def emoji(self, ctx: commands.Context, emoji: discord.PartialEmoji):
        if not emoji.is_custom_emoji():
            raise commands.BadArgument()

        await ctx.send(embed=PoppiEmbed()
                       .set_author(name=f":{emoji.name}:", url=emoji.url)
                       .set_image(url=emoji.url))

    @command(help="Send a support DM to my owner", usage="[message]")
    async def support(self, ctx: commands.Context, *, msg):
        user = await self.bot.fetch_user(self.bot.owner_id)
        await user.send(f"Support request from {ctx.author.name}#{ctx.author.discriminator}:\n\n{msg}")

        await ctx.send(embed=success_embed())
