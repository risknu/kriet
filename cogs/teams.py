from __future__ import annotations

import logging, json
from os import path, environ
import disnake
from disnake.ext import commands

class teams(commands.Cog):
    def __init__(self, bot: commands.Bot = None) -> None:
        self.bot: commands.Bot = bot
        
    @commands.slash_command(
        description="Send a whitelist request to the server")
    async def whitelist_request(self, inter: disnake.ApplicationCommandInteraction = None,
                                minecraft_nickname: str = None) -> None:
        logging.getLogger('kriet').debug(f"Account \"{inter.author.name}\" used command \"whitelist_request\".")
        if not path.exists("requests.json"):
            logging.getLogger("kriet").error("requests.json file not exist, please check path to file or create new")
            return None
        with open('requests.json', 'r') as fileIO_r:
            json_data: list[dict] = json.load(fileIO_r)
            json_data.append({
                "minecraft_nickname": minecraft_nickname,
                "can_join": False,
                "discord_info": {
                    "nick": inter.author.nick,
                    "name": inter.author.name,
                    "display_name": inter.author.display_name}})
        with open('requests.json', 'w') as fileIO_w:
            json.dump(json_data, fileIO_w, indent=4)
        await inter.response.send_message("Your request will be sent to moderation. Please wait until it is accepted for you to check, enter `/whitelist_status`")
        
    @commands.slash_command(
        description="Check the status of the request to the server")
    async def whitelist_status(self, inter: disnake.ApplicationCommandInteraction = None) -> None:
        logging.getLogger('kriet').debug(f"Account \"{inter.author.name}\" used command \"whitelist_status\".")
        if not path.exists("requests.json"):
            logging.getLogger("kriet").error("requests.json file not exist, please check path to file or create new")
            return None
        with open('requests.json', 'r') as fileIO_r:
            json_data: list[dict] = json.load(fileIO_r)
        for ite_, account in enumerate(json_data):
            if inter.author.name == account["discord_info"]["name"] or inter.author.display_name == account["discord_info"]["display_name"]:
                await inter.response.send_message(f"Your account is currently under {"**review**" if not account['can_join'] else "**accepted**"}")
                return None
        await inter.response.send_message("Your account was not found. Please register it")
        
def setup(bot: commands.Bot = None) -> None:
    bot.add_cog(teams(bot))
    