from __future__ import annotations

from misc import server_cls, server_request
from os import environ
import disnake
from disnake.ext import commands

class server(commands.Cog):
    def __init__(self, bot: commands.Bot = None) -> None:
        self.bot: commands.Bot = bot
        self.__server_info: server_cls = server_request(environ.get("SERVER_IP"), environ.get("SERVER_PORT"))
        
    @commands.slash_command(
        description="With this command, you can check the server latency")
    async def latency(self, inter: disnake.ApplicationCommandInteraction = None) -> None:
        latency: int | None = self.__server_info.latency
        await inter.response.send_message(f"The server latency is approximately `{latency if latency is not None else "empty"}`")
        
    @commands.slash_command(
        description="With this command, you can view the list of players on the server")
    async def players(self, inter: disnake.ApplicationCommandInteraction = None) -> None:
        players_names: int | None = self.__server_info.players_names
        max: int | None = self.__server_info.max_players
        now: int | None = self.__server_info.players_count
        await inter.response.send_message(f"List of players on the server `{now if now is not None else "~"}`/`{max if max is not None else "~"}`\n{"\n".join(players_names) if players_names is not None else "empty"}")
        
    @commands.slash_command(
        description="With this command, you can check the game version")
    async def version(self, inter: disnake.ApplicationCommandInteraction = None) -> None:
        version: str = self.__server_info.version
        await inter.response.send_message(f"Server version is `{version if version is not None else "empty"}`")
        
    @commands.slash_command(
        description="With this command, you can view information about the game")
    async def info(self, inter: disnake.ApplicationCommandInteraction = None) -> None:
        players_names: int | None = self.__server_info.players_names
        max: int | None = self.__server_info.max_players
        now: int | None = self.__server_info.players_count
        version: str = self.__server_info.version
        latency: int | None = self.__server_info.latency
        
        version: str = f"server version is `{version if version is not None else "empty"}`;"
        players: str = f"list of players on the server `{now if now is not None else "~"}`/`{max if max is not None else "~"}`\n{", ".join(players_names) if players_names is not None else "empty"};"        
        latency: str = f"the server latency is approximately `{latency if latency is not None else "empty"}`;"
        await inter.response.send_message(f"Server information; {version} {players} {latency}")

def setup(bot: commands.Bot = None) -> None:
    bot.add_cog(server(bot))
    