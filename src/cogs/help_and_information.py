from typing import Union

import discord
from discord.ext import commands
from discord.ext.commands import command

from poppi import success_embed, FetchedUser, Poppi


class HelpAndInformation(commands.Cog, name="Help and Information"):
    def __init__(self, bot: Poppi):
        self.bot = bot

    @command(help="Display the help", usage="")
    async def help(self, ctx):
        # Send the bot's help embed which is defined by update_help_embed() in /src/poppi.py
        self.bot.help_embed.set_footer(text=f"'?' means argument is optional")
        await ctx.send(embed=self.bot.help_embed)

    @command(help="Get someone's avatar", usage="[user|None]")
    async def avatar(self, ctx, user: Union[discord.User, FetchedUser] = None):
        # Return avatar of author if no user is given
        if user is None:
            user = ctx.author

        embed = discord.Embed(color=discord.Color.purple()) \
            .set_author(name=f"{user.display_name}'s avatar", url=str(user.avatar_url)) \
            .set_image(url=user.avatar_url)

        await ctx.send(embed=embed)

    @command(help="Send a support DM to my creator", usage="[message]")
    async def support(self, ctx, *, msg):
        user = await self.bot.fetch_user(self.bot.owner_id)
        await user.send(f"Support request from {ctx.author.name}#{ctx.author.discriminator}:\n\n{msg}")

        await ctx.send(embed=success_embed())
