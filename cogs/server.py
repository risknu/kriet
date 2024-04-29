from __future__ import annotations

from misc import server_cls, server_request
from os import environ
import disnake
from disnake.ext import commands, tasks

class server(commands.Cog):
    def __init__(self, bot: commands.Bot = None) -> None:
        self.bot: commands.Bot = bot
        self.__server_info: server_cls = server_request(environ.get("SERVER_IP"), environ.get("SERVER_PORT"))
        self.update_status.start()
        
    @tasks.loop(seconds=30)
    async def update_status(self):
        try:
            max: int | None = self.__server_info.max_players
            now: int | None = self.__server_info.players_count
            self.__server_info: server_cls = server_request(environ.get("SERVER_IP"), environ.get("SERVER_PORT"))
            await self.bot.change_presence(status=disnake.Status.online, activity=disnake.Activity(
                type=disnake.ActivityType.watching,
                name=f'Working! {now if now is not None else "~"}/{max if max is not None else "~"}'))
        except ConnectionRefusedError:
            await self.bot.change_presence(status=disnake.Status.dnd, activity=disnake.Activity(
                type=disnake.ActivityType.watching, name='Not Working!'))
        except Exception as e:
            await self.bot.change_presence(status=disnake.Status.idle, activity=disnake.Activity(
                type=disnake.ActivityType.watching, name='Connection ERR!'))

    @update_status.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()
        
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
    