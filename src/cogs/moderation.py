from discord.ext import commands
from discord.ext.commands import command, guild_only, has_guild_permissions
import discord


class Moderation(commands.Cog, name="Moderation"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @command(help="Ban a user")
    @guild_only()
    @has_guild_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User, *, reason="None"):
        try:
            await ctx.guild.ban(user, reason=reason)
            embed = discord.Embed(description="Success!", color=discord.Color.green())
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f"Couln't ban {user.display_name}!\n{str(e)}", color=discord.Color.green())
            await ctx.send(embed=embed, delete_after=5)

    @command(help="Softban a user")
    @guild_only()
    @has_guild_permissions(ban_members=True)
    async def softban(self, ctx, user: discord.User, *, reason="None"):
        try:
            await ctx.guild.ban(user, reason=reason)
            await ctx.guild.unban(user, reason=reason)
            embed = discord.Embed(description="Success!", color=discord.Color.green())
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f"Couln't softban {user.display_name}!\n{str(e)}", color=discord.Color.green())
            await ctx.send(embed=embed, delete_after=5)

    @command(help="Kick a user")
    @guild_only()
    @has_guild_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.User, *, reason="None"):
        try:
            await ctx.guild.kick(user, reason=reason)
            embed = discord.Embed(description="Success!", color=discord.Color.green())
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f"Couln't kick {user.display_name}!\n{str(e)}", color=discord.Color.green())
            await ctx.send(embed=embed, delete_after=5)

    @command(help="Clear up to 100 messages")
    @guild_only()
    @has_guild_permissions(manage_messages=True)
    async def clear(self, ctx, messages: int):
        if messages > 100:
            embed = discord.Embed(description="Please specify an amount <= 100!", color=discord.Color.green())
            return await ctx.send(embed=embed, delete_after=5)

        try:
            await ctx.channel.purge(limit=messages)
            embed = discord.Embed(description="Success!", color=discord.Color.green())
            await ctx.send(embed=embed, delete_after=5)
        except Exception as e:
            embed = discord.Embed(description=f"Couln't clear channel!\n{str(e)}", color=discord.Color.green())
            await ctx.send(embed=embed, delete_after=5)
