from __future__ import annotations

from misc import server_cls, server_protectc_request
from os import environ
import logging
import disnake
from disnake.ext import commands, tasks

class server(commands.Cog):
    def __init__(self, bot: commands.Bot = None) -> None:
        self.bot: commands.Bot = bot
        self.__is_working_now: bool = False
        logging.getLogger('kriet').debug(f"Server send request to Java")
        self.__server_info: server_cls = server_protectc_request(environ.get("SERVER_IP"), environ.get("SERVER_PORT"))
        logging.getLogger('kriet').debug(f"Request is checked")
        logging.getLogger('kriet').debug(f"Update wating; update_status.start()")
        self.update_status.start()
        logging.getLogger('kriet').debug(f"Update started; update_status.start()")
        
    @tasks.loop(seconds=30)
    async def update_status(self):
        try:
            max: int | None = self.__server_info.max_players
            now: int | None = self.__server_info.players_count
            logging.getLogger('kriet').debug(f"Server send request to Java")
            self.__server_info: server_cls = server_protectc_request(environ.get("SERVER_IP"), environ.get("SERVER_PORT"))
            logging.getLogger('kriet').debug(f"Request is checked")
            self.__is_working_now = True
            await self.bot.change_presence(status=disnake.Status.online, activity=disnake.Activity(
                type=disnake.ActivityType.watching,
                name=f'Working! {now if now is not None else "~"}/{max if max is not None else "~"}'))
        except ConnectionRefusedError:
            logging.getLogger('kriet').warning(f"Not Working! Update; update_status => ConnectionRefusedError")
            self.__is_working_now = False
            await self.bot.change_presence(status=disnake.Status.dnd, activity=disnake.Activity(
                type=disnake.ActivityType.watching, name='Not Working!'))
        except Exception as e:
            self.__is_working_now = False
            logging.getLogger('kriet').error(f"Not Working! Update; update_status => {e}")
            await self.bot.change_presence(status=disnake.Status.idle, activity=disnake.Activity(
                type=disnake.ActivityType.watching, name='Connection ERR!'))

    @update_status.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()
        
    @commands.slash_command(
        description="With this command, you can check the server latency")
    async def latency(self, inter: disnake.ApplicationCommandInteraction = None) -> None:
        latency: int | None = self.__server_info.latency
        logging.getLogger('kriet').debug(f"Account \"{inter.author.name}\" used command \"latency\".")
        await inter.response.send_message(f"The server latency is approximately `{round(float(latency)) if latency is not None else "~"}`")
        
    @commands.slash_command(
        description="With this command, you can view the list of players on the server")
    async def players(self, inter: disnake.ApplicationCommandInteraction = None) -> None:
        logging.getLogger('kriet').debug(f"Account \"{inter.author.name}\" used command \"players\".")
        players_names: int | None = self.__server_info.players_names
        max: int | None = self.__server_info.max_players
        now: int | None = self.__server_info.players_count
        await inter.response.send_message(f"List of players on the server `{now if now is not None else "~"}`/`{max if max is not None else "~"}`\n```diff\n{"\n".join([f'+ {player}' for player in players_names]) if players_names is not None else "- empty"}```")
        
    @commands.slash_command(
        description="With this command, you can check the game version")
    async def version(self, inter: disnake.ApplicationCommandInteraction = None) -> None:
        logging.getLogger('kriet').debug(f"Account \"{inter.author.name}\" used command \"version\".")
        version: str = self.__server_info.version
        await inter.response.send_message(f"Server version is `{version if version is not None else "x.y.z"}`")
        
    @commands.slash_command(
        description="With this command, you can view information about the game")
    async def info(self, inter: disnake.ApplicationCommandInteraction = None) -> None:
        logging.getLogger('kriet').debug(f"Account \"{inter.author.name}\" used command \"info\".")
        players_names: int | None = self.__server_info.players_names
        max: int | None = self.__server_info.max_players
        now: int | None = self.__server_info.players_count
        version: str = self.__server_info.version
        latency: int | None = self.__server_info.latency
        
        online_boolean: str = f"{"Working!" if self.__is_working_now else "Not Working!"}"
        version: str = f"server version is `{version if version is not None else "x.y.z"}`;"
        players: str = f"list of players on the server `{now if now is not None else "~"}`/`{max if max is not None else "~"}`\n{", ".join([f'`{player}`' for player in players_names]) if players_names is not None else "`empty`"};"        
        latency: str = f"the server latency is approximately `{round(float(latency)) if latency is not None else "empty"}`;"
        await inter.response.send_message(f"Status `{online_boolean}`; Server information; {version} {players} {latency}")

def setup(bot: commands.Bot = None) -> None:
    bot.add_cog(server(bot))
    