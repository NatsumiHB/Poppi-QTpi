from inspect import signature

import discord
from discord.ext import commands
from discord.ext.commands import group

from poppi import Poppi, PoppiEmbed
from poppi_helpers import success_embed


class Profile(commands.Cog, name="Profile"):
    def __init__(self, bot: Poppi):
        self.bot = bot

    @group(help="See a profile", usage="[user|None]", invoke_without_command=True)
    async def profile(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        create_on_not_found = member.id == ctx.author.id

        profile = self.bot.profile_helpers.get_or_create_profile(member.id, create_on_not_found)
        profile_author = f"{profile['nickname']} ({member.name})" if profile["nickname"] is not None else member.name

        avatar_url = profile["avatar_url"]

        if avatar_url is None \
                or await self.bot.profile_helpers.is_valid_avatar(avatar_url) is False:
            avatar_url = member.avatar_url

        await ctx.send(embed=PoppiEmbed()
                       .set_author(name=f"Profile of {profile_author}", icon_url=member.avatar_url)
                       .set_thumbnail(url=avatar_url)
                       .add_field(name="Profile description",
                                  value=profile["description"] or "No description set",
                                  inline=False)
                       .add_field(name="Balance",
                                  value=f"{profile['money']} {self.bot.config.money_config['currency']}",
                                  inline=True)
                       .add_field(name="Inventory",
                                  value=", ".join(
                                      self.bot.profile_helpers.get_item_by_id(item_id)["emoji"]
                                      for item_id
                                      in profile["inventory"]
                                      if len(profile["inventory"]) > 0
                                  ),
                                  inline=True))

    @profile.command(help="Set your nickname", usage="[string]")
    async def nickname(self, ctx: commands.Context, *, nickname: str):
        await self.bot.profile_helpers.set_profile_key(ctx.author.id, "nickname", nickname)

        await ctx.send(embed=success_embed(f"Successfully changed nickname to `{nickname}`"))

    # The name of the command function can't be description as that would override a discord.py function
    @profile.command(name="description", help="Set your description", usage="[string]")
    async def set_description(self, ctx: commands.Context, *, description: str):
        await self.bot.profile_helpers.set_profile_key(ctx.author.id, "description", description)

        await ctx.send(embed=success_embed(f"Successfully changed description to `{description}`"))

    @profile.command(help="Set your avatar", usage="[string|image]")
    async def avatar(self, ctx: commands.Context, *, avatar_url: str = None):
        if avatar_url is None:
            if len(ctx.message.attachments) > 0:
                avatar_url = ctx.message.attachments[0].url
            else:
                raise commands.MissingRequiredArgument([p for p in signature(self.avatar).parameters.values()][-1])

        await self.bot.profile_helpers.set_profile_key(ctx.author.id, "avatar_url", avatar_url)

        await ctx.send(embed=success_embed("Successfully changed avatar"))
