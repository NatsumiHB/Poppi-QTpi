import discord
from discord.ext import commands
from discord.ext.commands import command, guild_only, has_guild_permissions

from poppi import success_embed, Poppi


class Roles(commands.Cog, name="Roles"):
    def __init__(self, bot: Poppi):
        self.bot = bot

    @command(help="Get role information", usage="[role]")
    @guild_only()
    async def roleinfo(self, ctx, *, role: discord.Role):
        perm_string = f"\n\n```\n{', '.join(perm for (perm, value) in role.permissions.__iter__() if value == True)}```"
        embed = discord.Embed(title=f"Information about {role.name}",
                              description=f"ID: {role.id}\n"
                                          f"Color: 0x{role.color().value:X}\n\n"
                                          f"Mentionable: {role.mentionable}\n"
                                          f"Hoisted: {role.hoist}\n"
                                          f"Position: {role.position}\n"
                                          f"Members: {len(role.members)}"
                                          f"{perm_string if role.permissions.value > 0 else ''}",
                              color=role.color)
        await ctx.send(embed=embed)

    @command(help="Create a color role", usage="[color] [name]")
    @guild_only()
    @has_guild_permissions(manage_roles=True)
    async def ccr(self, ctx, color: discord.Color, *, name: str):
        role = await ctx.guild.create_role(name=name, colour=color)
        await ctx.send(embed=success_embed(f"Successfully created role {role.name}", color=role.color))

    @command(help="Delete a role", usage="[role]")
    @guild_only()
    @has_guild_permissions(manage_roles=True)
    async def dr(self, ctx, role: discord.Role):
        await role.delete()

    @command(help="Assign a role", usage="[member] [role]")
    @guild_only()
    @has_guild_permissions(manage_roles=True)
    async def ar(self, ctx, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(embed=success_embed(f"Successfully added {role.name} to {member.display_name}",
                                           color=role.color))

    @command(help="Remove a role", usage="[member] [role]")
    @guild_only()
    @has_guild_permissions(manage_roles=True)
    async def rr(self, ctx, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await ctx.send(embed=success_embed(f"Successfully removed {role.name} to {member.display_name}",
                                           color=role.color))
