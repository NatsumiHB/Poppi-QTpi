from discord.ext import commands
from discord.ext.commands import command

from poppi import Poppi
from poppi_helpers import success_embed, PoppiEmbed


class Money(commands.Cog, name="Profile"):
    def __init__(self, bot: Poppi):
        self.bot = bot

    @command(help="View the store", usage="")
    async def store(self, ctx: commands.Context):
        await ctx.send(embed=self.bot.store_embed)

    @command(help="Redeem your daily money", usage="")
    async def daily(self, ctx: commands.Context):
        self.bot.profile_helpers.redeem_daily(ctx.author.id)

        await ctx.send(embed=success_embed(f"Successfully redeemed your daily "
                                           f"{self.bot.config.money_config['currency']}"))

    @command(help="See your current balance", usage="")
    async def balance(self, ctx: commands.Context):
        profile = self.bot.profile_helpers.get_or_create_profile(ctx.author.id, create_on_not_found=True)

        await ctx.send(embed=PoppiEmbed(
            title="Balance",
            description=f"You got {profile['money']} {self.bot.config.money_config['currency']}")
        )

    @command(help="Buy an item", usage="[Item ID]")
    async def buy(self, ctx: commands.Context, item_id: int):
        item = self.bot.profile_helpers.get_item_by_id(item_id)

        self.bot.profile_helpers.buy_item(ctx.author.id, item)

        await ctx.send(embed=success_embed(f"Successfully bought one {item['name']}"))
