from inspect import signature

import discord
from discord.ext import commands
from discord.ext.commands import group, command

from poppi import Poppi, PoppiEmbed
from poppi_helpers import success_embed, error_embed, PoppiError


class Profile(commands.Cog, name="Profile"):
    def __init__(self, bot: Poppi):
        self.bot = bot

    @group(help="See a profile", usage="[user|None]", invoke_without_command=True)
    async def profile(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author

        profile = self.bot.profile_helpers.get_or_create_profile(member.id, create_on_not_found=True)
        # profile_author = f"{profile['nickname']} ({member.name})" if profile["nickname"] is not None else member.name
        #
        # avatar_url = profile["avatar_url"]

        # if avatar_url is None \
        #         or await self.bot.profile_helpers.is_valid_avatar(avatar_url) is False:
        #     avatar_url = member.avatar_url

        partner = (await self.bot.fetch_user(profile["partner"])).display_name if profile["partner"] is not None \
            else "None"

        await ctx.send(embed=PoppiEmbed()
                       .set_author(name=f"Profile of {member.display_name}")
                       .set_thumbnail(url=member.avatar_url)
                       # .add_field(name="Profile description",
                       #            value=profile["description"] or "No description set",
                       #            inline=False)
                       .add_field(name="Partner",
                                  value=partner,
                                  inline=True)
                       .add_field(name="Balance",
                                  value=f"{profile['money']} {self.bot.config.money_config['currency']}",
                                  inline=True)
                       .add_field(name="Inventory",
                                  value=", ".join(
                                      self.bot.profile_helpers.get_item_by_id(item_id)["emoji"]
                                      for item_id
                                      in profile["inventory"]
                                      if len(profile["inventory"]) > 0
                                  ) or "Empty",
                                  inline=True))

    # @profile.command(help="Set your nickname", usage="[string]")
    # async def nickname(self, ctx: commands.Context, *, nickname: str):
    #     await self.bot.profile_helpers.set_profile_key(ctx.author.id, "nickname", nickname)
    #
    #     await ctx.send(embed=success_embed(f"Successfully changed nickname to `{nickname}`"))
    #
    # # The name of the command function can't be description as that would override a discord.py function
    # @profile.command(name="description", help="Set your description", usage="[string]")
    # async def set_description(self, ctx: commands.Context, *, description: str):
    #     await self.bot.profile_helpers.set_profile_key(ctx.author.id, "description", description)
    #
    #     await ctx.send(embed=success_embed(f"Successfully changed description to `{description}`"))
    #
    # @profile.command(help="Set your avatar", usage="[string|image]")
    # async def avatar(self, ctx: commands.Context, *, avatar_url: str = None):
    #     if avatar_url is None:
    #         if len(ctx.message.attachments) > 0:
    #             avatar_url = ctx.message.attachments[0].url
    #         else:
    #             raise commands.MissingRequiredArgument([p for p in signature(self.avatar).parameters.values()][-1])
    #
    #     await self.bot.profile_helpers.set_profile_key(ctx.author.id, "avatar_url", avatar_url)
    #
    #     await ctx.send(embed=success_embed("Successfully changed avatar"))

    @command(help="Marry someone", usage="[Member]")
    async def marry(self, ctx: commands.Context, member: discord.Member):
        def check(m: discord.Message):
            return m.author == member and m.channel == ctx.channel

        if self.bot.profile_helpers \
                .inventory_item_count(ctx.author.id,
                                      self.bot.profile_helpers.get_item_by_name("Wedding Ring")["id"]) == 0:
            raise PoppiError("You need a wedding ring to marry someone!")

        await ctx.send(f"{member.mention}, do you want to marry {ctx.author.mention}? (yes/no)\n\n"
                       f"**If someone else replies before you or you reply with something different than yes/no "
                       f"the command will cancel. This will be fixed in a future update.**")

        response = await self.bot.wait_for("message", check=check, timeout=20)
        if response.content.lower() == "yes":
            self.bot.profile_helpers.marry(ctx.author.id, member.id)

            await ctx.send(embed=success_embed(f"You two are now married!"))
        elif response.content.lower() == "no":
            await ctx.send(embed=error_embed(f"{member.display_name} did not accept the proposal!"))

    @command(help="Divorce from your current partner", usage="")
    async def divorce(self, ctx: commands.Context):
        profile = self.bot.profile_helpers.get_or_create_profile(ctx.author.id, create_on_not_found=True)

        if profile["partner"] is None:
            raise PoppiError("You aren't married to anyone!")

        partner = await self.bot.fetch_user(profile["partner"])

        def check(m: discord.Message):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send(f"Are you sure you want to divorce from {partner.display_name}? (yes/no)\n\n"
                       f"**If someone else replies before you or you reply with something different than yes/no "
                       f"the command will cancel. This will be fixed in a future update.**")

        response = await self.bot.wait_for("message", check=check, timeout=20)
        if response.content.lower() == "yes":
            self.bot.profile_helpers.divorce(ctx.author.id)

            await ctx.send(embed=success_embed(f"You and {partner.display_name} are now divorced!"))
        elif response.content.lower() == "no":
            await ctx.send(embed=error_embed(f"Canceled divorce!"))
