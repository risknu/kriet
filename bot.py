from __future__ import annotations

import disnake
from disnake.ext import commands

import logging
from misc import configure_logs
configure_logs()

from os import environ, listdir
from dotenv import load_dotenv
load_dotenv()

logging.getLogger('kriet').debug("Setting up project intents.")
intents: disnake.Intents = disnake.Intents.all()
logging.getLogger('kriet').debug("Configuring the bot for the project with intent loading.")
bot: commands.Bot = commands.Bot(command_prefix="?", intents=intents)

for ite, file in enumerate(listdir("./cogs/")):
    if not file.endswith('.py'): continue
    logging.getLogger('kriet').debug(f"Loading a cog under the name \"{file.split(".")[0]}\".")
    bot.load_extension(f"cogs.{file.split(".")[0]}")
    logging.getLogger('kriet').debug(f"Successfully added and retrieved cog \"{file.split(".")[0]}\".")

if __name__ == "__main__":
    logging.getLogger('kriet').debug("The project is launching.")
    bot.run(environ.get("TOKEN")) 
