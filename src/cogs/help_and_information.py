from typing import Union

import discord
from discord.ext import commands
from discord.ext.commands import command
from disputils import BotEmbedPaginator

from poppi import Poppi, PoppiEmbed
from poppi_helpers import FetchedUser, success_embed


class HelpAndInformation(commands.Cog, name="Help and Information"):
    def __init__(self, bot: Poppi):
        self.bot = bot

    @command(help="Display the help", usage="")
    async def help(self, ctx: commands.Context):
        # The embed generator for the help embeds is in /src/poppi.py
        await BotEmbedPaginator(ctx, self.bot.help_embeds).run()

    @command(help="Get someone's avatar", usage="[user|None]")
    async def avatar(self, ctx: commands.Context, user: Union[discord.User, FetchedUser] = None):
        # Return avatar of author if no user is given
        user = user or ctx.author

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
        await user.send(f"Support request from {ctx.author.name}#{ctx.author.discriminator} "
                        f"({ctx.author.mention}, ID: {ctx.author.id}):"
                        f"\n\n{msg}")

        await ctx.send(embed=success_embed())
