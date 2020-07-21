import aiohttp


class APIUtils:
    def __init__(self):
        self.client_session = aiohttp.ClientSession()

    async def get_json_response(self, url: str):
        async with self.client_session.get(url) as r:
            return await r.json()

    async def get_ram_gif(self, kind: str):
        image = await self.get_json_response(f"https://rra.ram.moe/i/r?type={kind}")
        return f"https://cdn.ram.moe/{image['path'][3:]}"

    async def get_waifu(self):
        res = await self.get_json_response("https://waifus-are.fun-stuff.xyz/get_json")
        return res["id"], res["url"]

    async def get_random_cat(self):
        image = await self.get_json_response("https://api.thecatapi.com/v1/images/search")
        return image[0]["url"]
