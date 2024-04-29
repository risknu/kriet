from __future__ import annotations

import disnake
from disnake.ext import commands

from os import environ, listdir
from dotenv import load_dotenv
load_dotenv()

intents: disnake.Intents = disnake.Intents.all()
bot: commands.Bot = commands.Bot(command_prefix="?", intents=intents)

for ite, file in enumerate(listdir("./cogs/")):
    if not file.endswith('.py'): continue
    bot.load_extension(f"cogs.{file.split(".")[0]}")

bot.run(environ.get("TOKEN")) 
