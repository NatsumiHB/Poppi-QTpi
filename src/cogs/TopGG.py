import logging
import os

import dbl
from discord.ext import commands


class TopGG(commands.Cog, name="TopGG"):
    def __init__(self, bot):
        self.bot = bot
        self.token = os.getenv("POPPI_DBL_TOKEN")
        if self.token != "debug":
            self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)

    @commands.Cog.listener()
    async def on_guild_post(self):
        logging.info("Guild count posted successfully")
