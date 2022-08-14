import disnake
from bot import ext
from bot.config import Config
from disnake.ext import commands


class AdminConfirm(disnake.ui.View):
    """UI buttons components for confirmations"""

    def __init__(self, bot) -> None:
        # init view with timeout of 15 seconds
        super().__init__(timeout=15)
        self.bot = bot

    @disnake.ui.button(
        label="Yes, edit the embed already!", style=disnake.ButtonStyle.success
    )
    async def confirm(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ) -> None:
        """Confirm button - refreshes the welcome message embed"""

        # update the welcome message embed
        message_id = ext.get_welcome_message()
        if not message_id:
            # welcome message has not been sent yet
            for c in self.children:
                c.disabled = True

            return await interaction.response.edit_message(
                "I tried, but failed because there is no welcome message sent yet. Restart me and it should appear shortly after.",
                view=self,
            )

        # get channel, message, and embed data from configs
        channel = await self.bot.fetch_channel(Config.welcome_channel_id)
        guild = channel.guild
        message = await channel.fetch_message(message_id)
        embed = ext.get_welcome_embed()

        # create embed
        embed = disnake.Embed.from_dict(embed)
        embed.title = embed.title.replace("{GUILDNAME}", guild.name)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else disnake.Embed.Empty)

        # edit the welcome message with new embed
        await message.edit(embed=embed)

        # respond to the button interaction
        for c in self.children:
            c.disabled = True

        await interaction.response.edit_message(
            "Aye, aye, captain <:blobsalute:929897251197833266>", view=self
        )

    @disnake.ui.button(label="No, I forgot :/", style=disnake.ButtonStyle.danger)
    async def cancel(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ) -> None:
        """Cancel updating of welcome message"""

        for c in self.children:
            c.disabled = True

        await interaction.response.edit_message(
            "Let me know when you've updated that file and we can try again", view=self
        )


class Admin(commands.Cog):
    """Extension class for adding Admin related commands/events to the bot"""

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"Extension loaded: {self.qualified_name}")

    @commands.slash_command(name="update_welcome")
    @commands.has_permissions(administrator=True)
    async def update_welcome(
        self, interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        """Update the welcome message - run after updating the welcome_message.json"""

        await interaction.response.send_message(
            'Did you remember to edit the embed in "/data/welcome_embed.json"?',
            view=AdminConfirm(self.bot),
            ephemeral=True,
        )

    @update_welcome.error
    async def welcome_permission_error(
        self, interaction: disnake.ApplicationCommandInteraction, error
    ) -> None:
        """Catch errors for the update_welcome command"""

        if isinstance(error, commands.MissingPermissions):
            return await interaction.response.send_message(
                "You're not quite powerful enough to use this command.", ephemeral=True
            )

        # raise other errors
        raise error
