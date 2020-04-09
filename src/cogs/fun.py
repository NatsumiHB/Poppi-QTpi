from discord.ext import commands
from discord.ext.commands import command, guild_only
import discord
import requests


def get_ram_gif(kind: str):
    res = requests.get(f"https://rra.ram.moe/i/r?type={kind}").json()
    gif = res["path"]
    return f"https://cdn.ram.moe/{gif[3:]}"


def get_ram_embed(kind, verb, author: discord.Member, member: discord.Member):
    name = "themselves" if member == author else member.display_name
    embed = discord.Embed(title=f"{author.display_name} {verb} {name}!", color=discord.Color.purple())
    embed.set_image(url=get_ram_gif(kind))
    return embed


class Fun(commands.Cog, name="Fun"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Lots of repeated code for RP GIF commands
    @command(help="Hug someone", usage="[mention]")
    @guild_only()
    async def hug(self, ctx, member: discord.Member):
        await ctx.send(embed=get_ram_embed("hug", "hugs", ctx.author, member))

    @command(help="Pat someone", usage="[mention]")
    @guild_only()
    async def pat(self, ctx, member: discord.Member):
        await ctx.send(embed=get_ram_embed("pat", "pats", ctx.author, member))

    @command(help="Slap someone", usage="[mention]")
    @guild_only()
    async def slap(self, ctx, member: discord.Member):
        await ctx.send(embed=get_ram_embed("slap", "slaps", ctx.author, member))

    @command(help="Kiss someone", usage="[mention]")
    @guild_only()
    async def kiss(self, ctx, member: discord.Member):
        await ctx.send(embed=get_ram_embed("kiss", "kisses", ctx.author, member))

    @command(help="Lewd someone", usage="[mention]")
    @guild_only()
    async def lewd(self, ctx, member: discord.Member):
        await ctx.send(embed=get_ram_embed("lewd", "lewds", ctx.author, member))

    @command(help="Lick someone", usage="[mention]")
    @guild_only()
    async def lick(self, ctx, member: discord.Member):
        await ctx.send(embed=get_ram_embed("lick", "licks", ctx.author, member))

    @command(help="Cuddle someone", usage="[mention]")
    @guild_only()
    async def cuddle(self, ctx, member: discord.Member):
        await ctx.send(embed=get_ram_embed("cuddle", "cuddles", ctx.author, member))

    @command(help="OwO at someone", usage="[mention]")
    @guild_only()
    async def owo(self, ctx, member: discord.Member):
        await ctx.send(embed=get_ram_embed("owo", "owos at", ctx.author, member))

    @command(help="Meow at someone", usage="[mention]")
    @guild_only()
    async def meow(self, ctx, member: discord.Member):
        await ctx.send(embed=get_ram_embed("nyan", "meows at", ctx.author, member))

    @command(help="Nom someone", usage="[mention]")
    @guild_only()
    async def nom(self, ctx, member: discord.Member):
        await ctx.send(embed=get_ram_embed("nom", "noms", ctx.author, member))
