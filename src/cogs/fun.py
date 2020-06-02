from discord.ext import commands
from discord.ext.commands import command, guild_only
import discord
import aiohttp
import typing


class Fun(commands.Cog, name="Fun"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client_session = aiohttp.ClientSession()

    async def get_ram_gif(self, kind: str):
        async with self.client_session.get(f"https://rra.ram.moe/i/r?type={kind}") as r:
            res = await r.json()
            return f"https://cdn.ram.moe/{res['path'][3:]}"

    async def get_ram_embed(self, kind, verb, author: discord.Member, member: typing.Union[discord.Member, str] = None):
        # Check who's being RP'd
        # Check if a member got pinged, set according to who got pinged
        if isinstance(member, discord.Member):
            if member == author:
                name = "themselves"
            elif member.id == self.bot.user.id:
                name = "me"
            else:
                name = member.display_name
        # Check for no argument or RP'd string is "me" -> user RPs themselves
        elif member == "me" or member is None:
            name = author.display_name
            author = author.guild.get_member(self.bot.user.id)
        # Same as first elif but for bot user
        elif member in ("you", "yourself", "poppi"):
            name = "me"
        # If it is a string that isn't "me" or "you" make the RP'd name the string
        else:
            name = member

        embed = discord.Embed(title=f"{author.display_name} {verb} {name}!", color=discord.Color.purple())
        embed.set_image(url=await self.get_ram_gif(kind))
        return embed

    # Lots of repeated code for RP GIF commands
    @command(help="Hug someone", usage="[mention|string|None]")
    @guild_only()
    async def hug(self, ctx, *, member: typing.Union[discord.Member, str] = None):
        await ctx.send(embed=await self.get_ram_embed("hug", "hugs", ctx.author, member))

    @command(help="Pat someone", usage="[mention|string|None]")
    @guild_only()
    async def pat(self, ctx, *, member: typing.Union[discord.Member, str] = None):
        await ctx.send(embed=await self.get_ram_embed("pat", "pats", ctx.author, member))

    @command(help="Slap someone", usage="[mention|string|None]")
    @guild_only()
    async def slap(self, ctx, *, member: typing.Union[discord.Member, str] = None):
        await ctx.send(embed=await self.get_ram_embed("slap", "slaps", ctx.author, member))

    @command(help="Kiss someone", usage="[mention|string|None]")
    @guild_only()
    async def kiss(self, ctx, *, member: typing.Union[discord.Member, str] = None):
        await ctx.send(embed=await self.get_ram_embed("kiss", "kisses", ctx.author, member))

    @command(help="Lewd someone", usage="[mention|string|None]")
    @guild_only()
    async def lewd(self, ctx, *, member: typing.Union[discord.Member, str] = None):
        await ctx.send(embed=await self.get_ram_embed("lewd", "lewds", ctx.author, member))

    @command(help="Lick someone", usage="[mention|string|None]")
    @guild_only()
    async def lick(self, ctx, *, member: typing.Union[discord.Member, str] = None):
        await ctx.send(embed=await self.get_ram_embed("lick", "licks", ctx.author, member))

    @command(help="Cuddle someone", usage="[mention|string|None]")
    @guild_only()
    async def cuddle(self, ctx, *, member: typing.Union[discord.Member, str] = None):
        await ctx.send(embed=await self.get_ram_embed("cuddle", "cuddles", ctx.author, member))

    @command(help="OwO at someone", usage="[mention|string|None]")
    @guild_only()
    async def owo(self, ctx, *, member: typing.Union[discord.Member, str] = None):
        await ctx.send(embed=await self.get_ram_embed("owo", "owos at", ctx.author, member))

    @command(help="Meow at someone", usage="[mention|string|None]")
    @guild_only()
    async def meow(self, ctx, *, member: typing.Union[discord.Member, str] = None):
        await ctx.send(embed=await self.get_ram_embed("nyan", "meows at", ctx.author, member))

    @command(help="Nom someone", usage="[mention|string|None]")
    @guild_only()
    async def nom(self, ctx, *, member: typing.Union[discord.Member, str] = None):
        await ctx.send(embed=await self.get_ram_embed("nom", "noms", ctx.author, member))
