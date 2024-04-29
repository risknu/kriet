from __future__ import annotations

from os import path, environ
import disnake
from disnake.ext import commands

class f_tag(commands.Cog):
    def __init__(self, bot: commands.Bot = None) -> None:
        self.bot: commands.Bot = bot
        
    @commands.slash_command(
        description="The ping command returns the time it takes for a server to respond")
    async def ping(self, inter: disnake.ApplicationCommandInteraction = None) -> None:
        await inter.response.send_message(f"Pong! `{round(self.bot.latency * 1000)}ms`")
        
    @commands.slash_command(
        description="The server info command provides information about the server that can be read")
    async def about(self, inter: disnake.ApplicationCommandInteraction = None) -> None:
        if not path.exists(environ.get("ABOUT_PATH")):
            await inter.response.send_message(f"**ERR=>**\nOops, looks like the bot is having trouble finding what's needed. Try again later\n`cogs.onready.f_tag.about.if[0]`")
            return None
        with open(environ.get("ABOUT_PATH"), 'r', encoding='utf-8') as fileIO_R:
            readed_ABOUT: str = fileIO_R.read()
        await inter.response.send_message(f"{str(readed_ABOUT)}")

def setup(bot: commands.Bot = None) -> None:
    bot.add_cog(f_tag(bot))
    