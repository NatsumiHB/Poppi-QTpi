import typing
from typing import Union

import discord
from discord.ext import commands
from discord.ext.commands import command
from disputils import BotEmbedPaginator

from poppi import Poppi, PoppiEmbed
from poppi_helpers import FetchedUser


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

    @command(help="Get information about someone", usage="[user]")
    async def userinfo(self, ctx: commands.Context, user: typing.Union[discord.User, FetchedUser] = None):
        if user is None:
            user = await self.bot.fetch_user(ctx.author.id)
            color = ctx.author.color
        else:
            color = user.color

        if ctx.guild is not None:
            member = await ctx.guild.fetch_member(user.id)

        embed = discord.Embed(title=f"Userinfo for {user.display_name}", color=color) \
            .set_thumbnail(url=user.avatar_url) \
            .add_field(name="ID", value=user.id, inline=False) \
            .add_field(name="Tag", value=f"{user.name}#{user.discriminator}", inline=False) \
            .add_field(name="Is Bot", value=user.bot, inline=False) \
            .add_field(name="Created at", value=str(user.created_at)[:-7], inline=False)

        if member is not None:
            embed.add_field(name="Joined at", value=str(member.joined_at)[:-7], inline=False)
            # embed.add_field(name="Online Status", value=member.raw_status.capitalize(), inline=False)

            if member.premium_since is not None:
                embed.add_field(name="Boosting since", value=member.premium_since, inline=False)

            embed.add_field(name="Roles", value=len(member.roles) - 1, inline=False)

            if len(member.activities) != 0:
                embed.add_field(name="Current Activities", value="\n".join(activity.name
                                                                           for activity
                                                                           in member.activities), inline=False)

        if len(user.public_flags.all()) != 0:
            embed.add_field(name="Badges", value=", ".join(
                str(flag)[10:].replace("_", " ").title()
                for flag
                in user.public_flags.all()
            ))

        await ctx.send(embed=embed)

    @command(help="Get a link to my GitHub repository", usage="")
    async def source(self, ctx: commands.Context):
        await ctx.send("https://poppi-bot.xyz/github")

    # @command(help="Send a support DM to my owner", usage="[message]")
    # async def support(self, ctx: commands.Context, *, msg):
    #     user = await self.bot.fetch_user(self.bot.owner_id)
    #     await user.send(f"Support request from {ctx.author.name}#{ctx.author.discriminator} "
    #                     f"({ctx.author.mention}, ID: {ctx.author.id}):"
    #                     f"\n\n{msg}")
    #
    #     await ctx.send(embed=success_embed())
