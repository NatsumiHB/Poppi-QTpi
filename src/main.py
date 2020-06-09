#!/usr/bin/python
import asyncio
import os
from threading import Thread

import coloredlogs
import discord
import waitress
from flask import Flask, redirect

from cogs.TopGG import TopGG
from cogs.events import Events
from cogs.fun import Fun
from cogs.help_and_information import HelpAndInformation
from cogs.moderation import Moderation
from cogs.roles import Roles
from poppi import Poppi

# Set up logging
coloredlogs.install(level="INFO", fmt="[%(asctime)s][%(levelname)s]: %(message)s")


# Set up bot
bot = Poppi(command_prefix=os.getenv("POPPI_PREFIX"),
            activity=discord.Game(name=f"{os.getenv('POPPI_PREFIX')}help"),
            owner_id=os.getenv("POPPI_OWNER_ID"))

bot.remove_command("help")
bot.add_cog(Events(bot))
bot.add_cog(HelpAndInformation(bot))
bot.add_cog(Moderation(bot))
bot.add_cog(Roles(bot))
bot.add_cog(Fun(bot))
bot.add_cog(TopGG(bot))

# Set up web API
api = Flask("Poppi QTπ")


@api.route("/server_count", methods=["GET"])
def server_count():
    return str(len(bot.guilds))


@api.route("/avatar", methods=["GET"])
def server_cont():
    return redirect(bot.user.avatar_url)


@api.route("/avatar_url", methods=["GET"])
def avatar_url():
    return str(bot.user.avatar_url)


@api.route("/commands", methods=["GET"])
def commands():
    return bot.commands_json


# Run API
Thread(target=waitress.serve, args=(api,), kwargs=dict(host="0.0.0.0", port=5000)).start()

# Run bot
loop = asyncio.get_event_loop()
loop.create_task(bot.run(os.getenv("POPPI_TOKEN")))
Thread(target=loop.run_forever).start()
