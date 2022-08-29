from datetime import datetime
from sys import version

import disnake
from disnake import __version__ as disnake_version
from disnake.ext import commands

from bot import __version__ as bot_version
from bot.cogs import Admin

# declare gateway intents
intents = disnake.Intents.none()
intents.guilds = True
intents.members = True
intents.guild_messages = True

bot = commands.InteractionBot(intents=intents)


@bot.listen()
async def on_ready() -> None:
    print(
        f"Bot Started at {datetime.now().strftime('%m-%d-%Y %H:%M')}\n"
        f"Disnake version: {disnake_version}\n"
        f"System: {version}\n"
        f"Bot Version: {bot_version}\n"
        f"Bot Name: {bot.user.name}\n"
        f"Bot ID: {bot.user.id}\n"
        f"Latency Status: {bot.latency:.2f}s\n"
        "----------------------------------------------------------------"
    )


# add bot extensions/cogs
bot.add_cog(Admin(bot))
