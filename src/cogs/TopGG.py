import dbl
from discord.ext import commands
import logging
import os


class TopGG(commands.Cog, name="TopGG"):
    def __init__(self, bot):
        self.bot = bot
        self.token = os.getenv("POPPI_DBL_TOKEN")
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)

    @commands.Cog.listener()
    async def on_guild_post(self):
        logging.info("Guild count posted successfully")
