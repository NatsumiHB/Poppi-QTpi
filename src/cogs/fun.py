import typing

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import command, guild_only

from poppi import Poppi


class Fun(commands.Cog, name="Fun"):
    def __init__(self, bot: Poppi):
        self.bot = bot
        self.client_session = aiohttp.ClientSession()

    async def get_ram_gif(self, kind: str):
        # Use the cog's ClientSession to get a gif and return the URL to that
        async with self.client_session.get(f"https://rra.ram.moe/i/r?type={kind}") as r:
            res = await r.json()
            return f"https://cdn.ram.moe/{res['path'][3:]}"

    # args is a string in order to use that if no mentions are given
    # Mentions do not interfere with strings which means args can be ignored
    # if pings are existent
    async def get_ram_embed(self, kind, verb, ctx: commands.Context, args: str = None):
        # Set author and first_pinged helper variable for later
        author = ctx.author
        first_pinged = ctx.message.mentions[0] if len(ctx.message.mentions) == 1 else None

        # Check who's being RP'd
        # Check if multiple members got pinged, set name to a comma-delimited list of them
        if len(ctx.message.mentions) > 1:
            name = ", ".join(member.display_name for member in ctx.message.mentions)
        # Check if a member got pinged, set according to who got pinged and context
        elif first_pinged is not None:
            if first_pinged == author:
                name = "themselves"
            elif first_pinged.id == self.bot.user.id:
                name = "me"
            else:
                name = first_pinged.display_name
        # Check for no argument or RP'd string is "me" -> user RPs themselves
        elif args == "me" or args is None:
            name = author.display_name
            author = ctx.author.guild.get_member(self.bot.user.id)
        # Same as first elif but for bot user
        elif args in ("you", "yourself", "poppi"):
            name = "me"
        # If it is a string that isn't "me" or "you" make the RP'd name the string
        else:
            name = args

        embed = discord.Embed(title=f"{author.display_name} {verb} {name}!", color=discord.Color.purple())
        embed.set_image(url=await self.get_ram_gif(kind))
        return embed

    # Lots of repeated code for RP GIF commands
    @command(help="Hug someone", usage="[mention|string|None]")
    @guild_only()
    async def hug(self, ctx, *, args: str = None):
        await ctx.send(embed=await self.get_ram_embed("hug", "hugs", ctx, args))

    @command(help="Pat someone", usage="[mention|string|None]")
    @guild_only()
    async def pat(self, ctx, *, args: str = None):
        await ctx.send(embed=await self.get_ram_embed("pat", "pats", ctx, args))

    @command(help="Slap someone", usage="[mention|string|None]")
    @guild_only()
    async def slap(self, ctx, *, args: str = None):
        await ctx.send(embed=await self.get_ram_embed("slap", "slaps", ctx, args))

    @command(help="Kiss someone", usage="[mention|string|None]")
    @guild_only()
    async def kiss(self, ctx, *, args: str = None):
        await ctx.send(embed=await self.get_ram_embed("kiss", "kisses", ctx, args))

    @command(help="Lewd someone", usage="[mention|string|None]")
    @guild_only()
    async def lewd(self, ctx, *, args: str = None):
        await ctx.send(embed=await self.get_ram_embed("lewd", "lewds", ctx, args))

    @command(help="Lick someone", usage="[mention|string|None]")
    @guild_only()
    async def lick(self, ctx, *, args: str = None):
        await ctx.send(embed=await self.get_ram_embed("lick", "licks", ctx, args))

    @command(help="Cuddle someone", usage="[mention|string|None]")
    @guild_only()
    async def cuddle(self, ctx, *, args: str = None):
        await ctx.send(embed=await self.get_ram_embed("cuddle", "cuddles", ctx, args))

    @command(help="OwO at someone", usage="[mention|string|None]")
    @guild_only()
    async def owo(self, ctx, *, args: str = None):
        await ctx.send(embed=await self.get_ram_embed("owo", "owos at", ctx, args))

    @command(help="Meow at someone", usage="[mention|string|None]")
    @guild_only()
    async def meow(self, ctx, *, args: str = None):
        await ctx.send(embed=await self.get_ram_embed("nyan", "meows at", ctx, args))

    @command(help="Nom someone", usage="[mention|string|None]")
    @guild_only()
    async def nom(self, ctx, *, args: str = None):
        await ctx.send(embed=await self.get_ram_embed("nom", "noms", ctx, args))
