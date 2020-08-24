import aiohttp
from discord.ext import commands


class APIUtils:
    def __init__(self):
        self.client_session = aiohttp.ClientSession()

    async def get_json_response(self, url: str):
        async with self.client_session.get(url) as r:
            if r.status == 404:
                raise commands.CommandInvokeError("\nAPI call returned 404 (Not Found)")

            return await r.json()

    async def get_ram_gif(self, kind: str):
        image = await self.get_json_response(f"https://rra.ram.moe/i/r?type={kind}")
        return f"https://cdn.ram.moe/{image['path'][3:]}"

    async def get_waifu(self, waifu_id: int):
        res = await self.get_json_response(f"https://waifus-are.fun-stuff.xyz/get_json"
                                           f"{f'/{waifu_id}' if waifu_id is not None else ''}")

        return res["id"], res["url"]

    async def get_random_cat(self):
        image = await self.get_json_response("https://api.thecatapi.com/v1/images/search")
        return image[0]["url"]
