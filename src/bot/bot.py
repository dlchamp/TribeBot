from datetime import datetime
from sys import version

from disnake import Embed, Game, Intents
from disnake import __version__ as disnake_version
from disnake.ext import tasks
from disnake.ext.commands import InteractionBot

from bot import __version__ as bot_version
from bot import ext
from bot.cogs import Admin
from bot.config import Config

intents = Intents.default()
bot = InteractionBot(intents=intents, activity=Game(name=""))


@bot.listen()
async def on_ready() -> None:
    print(
        f"Bot Started at {datetime.now().strftime('%m-%d-%Y %H:%M')}\n"
        f"Disnake version: {disnake_version}\n"
        f"System: {version}\n"
        f"Bot Version: {bot_version}\n"
        f"Bot Name: {bot.user.name}\n"
        f"Bot ID: {bot.user.id}\n"
        f"Latency Status: {bot.latency}s\n"
        "----------------------------------------------------------------"
    )

    # add persistent button for starting quiz
    bot.add_view(ext.StartQuiz())


# add bot extensions/cogs
bot.add_cog(Admin(bot))


@tasks.loop(count=1)
async def send_welcome_message() -> None:

    await bot.wait_until_ready()
    # get the welcome channel
    channel = bot.get_channel(int(Config.welcome_channel_id))
    guild = channel.guild

    welcome_message = ext.get_welcome_message()

    if welcome_message:
        # message has already been sent to the welcome channel
        return

    # message has not be sent
    # send message, then update config
    embed = ext.get_welcome_embed()
    embed = Embed.from_dict(embed)
    embed.title = embed.title.replace("{GUILDNAME}", guild.name)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else Embed.Empty)

    message = await channel.send(embed=embed, view=ext.StartQuiz())

    ext.update_message_sent(message.id)
