import discord
from discord.ext import commands
from discord.ext.commands import command, guild_only, has_guild_permissions

from poppi import success_embed, error_embed, Poppi, FetchedUser


class Moderation(commands.Cog, name="Moderation"):
    def __init__(self, bot: Poppi):
        self.bot = bot

    # Moderation commands
    # Errors are handled by the error handler in /src/main.py
    @command(help="Ban a user", usage="[user] [string|None]")
    @guild_only()
    @has_guild_permissions(ban_members=True)
    async def ban(self, ctx, user: FetchedUser, reason="None"):
        await ctx.guild.ban(user, reason=reason)

        await ctx.send(embed=success_embed(f"Successfully banned {user.display_name}#{user.discriminator}!"))

    @command(help="Unban a user", usage="[user] [string|None]")
    @guild_only()
    @has_guild_permissions(ban_members=True)
    async def unban(self, ctx, user: FetchedUser, reason="None"):
        await ctx.guild.unban(user, reason=reason)

        await ctx.send(embed=success_embed(f"Successfully unbanned {user.display_name}#{user.discriminator}!"))

    @command(help="Softban a user", usage="[member] [reason|None]")
    @guild_only()
    @has_guild_permissions(ban_members=True)
    async def softban(self, ctx, user: discord.Member, reason="None"):
        await ctx.guild.ban(user, reason=reason)
        await ctx.guild.unban(user, reason=reason)

        await ctx.send(embed=success_embed(f"Successfully softbanned {user.display_name}#{user.discriminator}!"))

    @command(help="Kick a user", usage="[member] [string|None]")
    @guild_only()
    @has_guild_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, reason="None"):
        await ctx.guild.kick(user, reason=reason)

        await ctx.send(embed=success_embed(f"Successfully kicked {user.display_name}#{user.discriminator}!"))

    @command(help="Clear up to 100 messages", usage="[amount]")
    @guild_only()
    @has_guild_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        # Check for boundaries (no more than 100 msgs deleted at once)
        if amount > 100:
            return await ctx.send(embed=error_embed("Please specify an amount <= 100!"))

        deleted = await ctx.channel.purge(limit=amount)

        await ctx.send(embed=success_embed(f"Deleted {len(deleted)} messages!"), delete_after=5)
