import discord
from discord.ext import commands
from discord.ext.commands import command

from poppi import success_embed, FetchedUser, Poppi


class HelpAndInformation(commands.Cog, name="Help and Information"):
    def __init__(self, bot: Poppi):
        self.bot = bot

    @command(help="Display this")
    async def help(self, ctx):
        embed = discord.Embed(title=f"Help for {self.bot.user.display_name}", color=discord.Color.purple())\
            .set_thumbnail(url=self.bot.user.avatar_url)\
            .set_footer(text=f"'?' means argument is optional | Up for {self.bot.get_formatted_uptime('{}d {}h {}m {}s')}")

        # Loop through all commands and cogs to generate help
        for cog in self.bot.cogs:
            if cog != "TopGG":
                bot_commands = ""
                for bot_command in self.bot.get_cog(cog).get_commands():
                    bot_commands += f"{bot_command.name} -> {bot_command.help}\n"

                embed.add_field(name=cog, value=bot_commands, inline=False)

        await ctx.send(embed=embed)

    @command(help="Get someone's avatar", usage="[mention?]")
    async def avatar(self, ctx, user: FetchedUser = None):
        # Return avatar of author if no user is given
        if user is None:
            user = ctx.author

        embed = discord.Embed(color=discord.Color.purple())\
            .set_author(name=f"{user.display_name}'s avatar", url=str(user.avatar_url))\
            .set_image(url=user.avatar_url)

        await ctx.send(embed=embed)

    @command(help="Send a support DM to my creator")
    async def support(self, ctx, *, msg):
        user = await self.bot.fetch_user(self.bot.owner_id)
        await user.send(f"Support request from {ctx.author.name}#{ctx.author.discriminator}:\n\n{msg}")

        await ctx.send(embed=success_embed())
