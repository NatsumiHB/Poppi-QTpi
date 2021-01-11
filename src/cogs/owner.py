import discord
from discord.ext import commands
from discord.ext.commands import command, is_owner

from poppi import Poppi
from poppi_helpers import success_embed


class Owner(commands.Cog, name="Owner"):
    def __init__(self, bot: Poppi):
        self.bot = bot

    @command(help="Reload all configs (this might break the store)", usage="")
    @is_owner()
    async def reload_config(self, ctx: commands.Context):
        await self.bot.reload_config()

        await ctx.send(embed=success_embed())

    @command(help="Reload the store", usage="")
    @is_owner()
    async def reload_store(self, ctx: commands.Context):
        await self.bot.reload_config()

        self.bot.store_items.empty()
        self.bot.load_store()
        self.bot.update_store_embed()

        await ctx.send(embed=success_embed())

    @command(help="Give someone money", usage="")
    @is_owner()
    async def give_money(self, ctx: commands.Context, user: discord.User, amount: int):
        self.bot.profile_helpers.get_or_create_profile(user.id, create_on_not_found=True)

        self.bot.profile_helpers.add_money(user.id, amount)

        await ctx.send(embed=success_embed(f"Successfully gave {user.display_name} {amount} "
                                           f"{self.bot.config.money_config['currency']}"))
