import shlex

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import command, guild_only, is_nsfw

from poppi import Poppi


# Function to create a proper name string from the names list
def set_name(ctx: commands.Context, names):
    # Join the names and only return the first name if only one is given
    name = " and ".join([", ".join(names[:-1]), names[-1]]) if len(names) > 1 else names[0]
    # Have bot RP the person if they tried to invoke the command on themselves
    return ctx.author.display_name if name == "themselves" else name


class Fun(commands.Cog, name="Fun"):
    def __init__(self, bot: Poppi):
        self.bot = bot
        self.client_session = aiohttp.ClientSession()

    async def get_ram_gif(self, kind: str):
        # Use the cog's ClientSession to get a gif and return the URL to that
        async with self.client_session.get(f"https://rra.ram.moe/i/r?type={kind}") as r:
            res = await r.json()
            return f"https://cdn.ram.moe/{res['path'][3:]}"

    # args has to be a string, when using a Union you can't easily parse it how it is currently implemented
    # The string element is ignored when mentions are present
    # Mentions do not interfere with strings which means args can be ignored
    # if pings are existent
    async def get_ram_embed(self, kind, verb, ctx: commands.Context, args: str = None):
        # Check who's being RP'd
        # Check if multiple members got pinged, set name to a comma-delimited list of them
        if len(ctx.message.mentions) > 0:
            # Generate a list of pinged users, using "themselves" if they pinged themselves,
            # "me" if the bot got pinged and the name of the pinged person for neither
            # It is turned into a list only containing one of each name/string
            names = list(dict.fromkeys(["themselves" if member.id == ctx.author.id else
                                        "me" if member.id == self.bot.user.id else
                                        member.display_name
                                        for member in ctx.message.mentions]))
            name = set_name(ctx, names)
        # Defaults to patting the user
        elif args is None:
            name = set_name(ctx, ["themselves"])
        # If there are no mentions, parse the arguments according to grammar using the
        # same method used when parsing pings, just applied to strings
        else:
            names = list(dict.fromkeys(["themselves" if name in ("me", "myself") or name == ctx.author.display_name else
                                        "me" if name in ("you", "poppi") else
                                        name
                                        for name in shlex.split(args)]))
            name = set_name(ctx, names)

        # Finally, set the author
        author = ctx.guild.get_member(self.bot.user.id) if name == ctx.author.display_name else ctx.author

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

    @command(help="Lewd someone (NSFW)", usage="[mention|string|None]")
    @guild_only()
    @is_nsfw()
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

    @command(help="OwO at someone (NSFW)", usage="[mention|string|None]")
    @guild_only()
    @is_nsfw()
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
