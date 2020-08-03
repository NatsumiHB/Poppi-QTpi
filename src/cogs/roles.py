from asyncio.exceptions import TimeoutError

import discord
import discord.ext.commands
from discord.ext import commands
from discord.ext.commands import command, guild_only, has_guild_permissions, bot_has_guild_permissions

from poppi import success_embed, Poppi


class Roles(commands.Cog, name="Roles"):
    def __init__(self, bot: Poppi):
        self.bot = bot

    @command(help="Get role information", usage="[role]")
    @guild_only()
    async def roleinfo(self, ctx: commands.Context, *, role: discord.Role):
        # Create a string using a generator that iterates over each permission and adds its name
        # Has two newlines in the beginning in order for the embed to render properly
        perm_string = f"\n\n```\n{', '.join(perm for (perm, value) in role.permissions.__iter__() if value == True)}```"

        info_embed = discord.Embed(title=f"Information about {role.name}",
                                   description=f"ID: {role.id}\n"
                                               f"Color: 0x{role.color.value:X}\n\n"
                                               f"Mentionable: {role.mentionable}\n"
                                               f"Hoisted: {role.hoist}\n"
                                               f"Position: {role.position}\n"
                                               f"Members: {len(role.members)}",
                                   color=role.color)

        if role.permissions.value > 0:
            info_embed.add_field(name="Permissions:", value=perm_string, inline=False)

        await ctx.send(embed=info_embed)

    @command(help="Create a color role", usage="[color] [name]")
    @guild_only()
    @has_guild_permissions(manage_roles=True)
    @bot_has_guild_permissions(manage_roles=True)
    async def ccr(self, ctx: commands.Context, color: discord.Color, *, name: str):
        role = await ctx.guild.create_role(name=name, color=color)
        await ctx.send(embed=success_embed(f"Successfully created role {role.name}", color=role.color))

    @command(help="Prompt to create a color role", usage="")
    @guild_only()
    @has_guild_permissions(manage_roles=True)
    @bot_has_guild_permissions(manage_roles=True)
    async def ccrp(self, ctx: commands.Context):
        # Check if the author and channel are the same as the ones of the original message
        # If lowercase message is "exit", abort command
        def check(m: discord.Message):
            return m.author == ctx.author and m.channel == ctx.channel

        async def abort_check(m: discord.Message):
            if m.content.lower() == "exit":
                await m.channel.send("Aborted!")
                return True

        # Override standard error handler in order to send a plaintext message on timeout
        # This is for consistency within the command
        try:
            # Prompt the user to enter a hex color
            await ctx.send("Started the role creation process.\n"
                           "**Which hex color should the role be?**\n"
                           "(You can always abort by typing \"exit\")")
            msg = await self.bot.wait_for("message", check=check, timeout=10)
            if await abort_check(msg):
                return
            color = discord.Color(int(msg.content, 16))

            # Prompt the user to enter a name for the role
            await ctx.send("What should the role be called?")
            msg = await self.bot.wait_for("message", check=check, timeout=10)
            if await abort_check(msg):
                return
            name = msg.content
        except TimeoutError as e:
            return await ctx.send("Command timed out!")

        role = await ctx.guild.create_role(name=name, color=color)
        await ctx.send(embed=success_embed(f"Successfully created role {role.name}", color=role.color))

    @command(help="Delete a role", usage="[role]")
    @guild_only()
    @has_guild_permissions(manage_roles=True)
    @bot_has_guild_permissions(manage_roles=True)
    async def dr(self, ctx: commands.Context, *, role: discord.Role):
        await role.delete()
        await ctx.send(embed=success_embed(f"Successfully deleted {role.name}", color=role.color))

    @command(help="Assign a role", usage="[member] [role]")
    @guild_only()
    @has_guild_permissions(manage_roles=True)
    @bot_has_guild_permissions(manage_roles=True)
    async def ar(self, ctx: commands.Context, member: discord.Member, *, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(embed=success_embed(f"Successfully added {role.name} to {member.display_name}",
                                           color=role.color))

    @command(help="Remove a role", usage="[member] [role]")
    @guild_only()
    @has_guild_permissions(manage_roles=True)
    @bot_has_guild_permissions(manage_roles=True)
    async def rr(self, ctx: commands.Context, member: discord.Member, *, role: discord.Role):
        await member.remove_roles(role)
        await ctx.send(embed=success_embed(f"Successfully removed {role.name} to {member.display_name}",
                                           color=role.color))
