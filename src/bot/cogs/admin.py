from typing import Optional

import disnake
from bot import ext
from bot.config import Config
from bot.quiz import Quiz
from disnake.ext import commands


class InvalidAttachmentType(Exception):
    """Special exception for invalid attachments"""

    pass


class AdminConfirm(disnake.ui.View):
    """UI buttons components for confirmations"""

    def __init__(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        embed: disnake.Embed,
        new: bool,
    ) -> None:
        # init view with timeout of 15 seconds
        super().__init__(timeout=15)
        self.interaction = interaction
        self.embed = embed
        self.new = new

        if self.new:
            self.add_item(
                disnake.ui.Button(
                    label="Send",
                    style=disnake.ButtonStyle.success,
                    custom_id="send_new_message",
                )
            )

        else:
            self.add_item(
                disnake.ui.Button(
                    label="Update",
                    style=disnake.ButtonStyle.success,
                    custom_id="update_message",
                )
            )

        self.add_item(
            disnake.ui.Button(
                label="Cancel", style=disnake.ButtonStyle.danger, custom_id="cancel"
            )
        )

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> None:
        """Callback for admin confirm buttons"""

        guild = interaction.guild
        button = interaction.component

        if button.custom_id == "cancel":
            await self.interaction.edit_original_message(
                "Aye aye. It's cancelled.", embed=None, view=self.clear_items()
            )
            return await interaction.response.defer(with_message=False)

        welcome_channel = await guild.fetch_channel(Config.welcome_channel_id)

        component = disnake.ui.Button(
            label="Start Quiz",
            style=disnake.ButtonStyle.primary,
            custom_id="start_quiz",
        )

        # message doesn't exist, sending new message
        if button.custom_id == "send_new_message":

            msg = await welcome_channel.send(embed=self.embed, components=[component])
            #  store the welcome message id in config
            ext.update_message_sent(msg.id)
            await self.interaction.edit_original_message(
                f"Welcome message has been sent to {welcome_channel.mention}",
                embed=None,
                view=self.clear_items(),
            )
            return await interaction.response.defer(with_message=False)

        if button.custom_id == "update_message":
            try:
                message = await welcome_channel.fetch_message(
                    ext.get_welcome_message_id()
                )
            except disnake.NotFound:
                # error because message was deleted, but not cleared from config's cache
                # null cache and send error message
                msg = await welcome_channel.send(
                    embed=self.embed, components=[component]
                )
                ext.update_message_sent(msg.id)
                return await self.interaction.edit_original_message(
                    "It looks like your welcome message was unintentionally deleted so I sent a new message and updated my local cache.",
                    embed=None,
                    view=self.clear_items(),
                )

            await message.edit(embed=self.embed)

            await self.interaction.edit_original_message(
                f"Your message in {welcome_channel.mention} has been updated",
                embed=None,
                view=self.clear_items(),
            )
            return await interaction.response.defer(with_message=False)


class Admin(commands.Cog):
    """Extension class for adding Admin related commands/events to the bot"""

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"Extension loaded: {self.qualified_name}")

    @commands.slash_command(name="view_tribe")
    @commands.has_permissions(administrator=True)
    async def view_tribe_embed(
        self, interaction: disnake.ApplicationCommandInteraction, tribe: str
    ):
        """View the embed for a specific tribe - used for testing changes

        Parameters
        ----------
        tribe: name of the tribe
        """
        tribe_short_name = tribe[0]  # just get first letter
        tribe_info = Config.tribes[tribe_short_name]
        embed = disnake.Embed(
            title=f"Welcome to the {tribe} Tribe!",
            description=f"{tribe_info['summary']}\n\nMembers of the **{tribe}** tribe are found to be:\n> {tribe_info['description']}",
        )
        embed.set_thumbnail(url=tribe_info["icon_url"])

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @view_tribe_embed.autocomplete("tribe")
    async def command_autocomplete(
        self, interaction: disnake.AppCommandInteraction, string: str
    ):
        string = string.lower()
        tribes = ["Mira", "Zuberi", "Briar", "Panuk"]
        return [tribe for tribe in tribes if string in tribe.lower()]

    @commands.slash_command(name="update_welcome")
    @commands.has_permissions(administrator=True)
    async def update_welcome(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        title: str,
        description: str,
        image: Optional[disnake.Attachment] = None,
        color: Optional[disnake.Colour] = None,
    ) -> None:
        """Update the welcome message or send the welcome message if not already sent

        Parameters
        ----------
        color: decimal representation of a color (https://tinyurl.com/embed-color)
        title: welcome message title
        description: welcome message description (long text)
        image: attach an image to be included with the message, leave blank to remove image
        """
        # create proper line breaks since parsed line breaks don't translate
        description = "\n".join(description.split(r"\n"))

        # create the embed
        embed = disnake.Embed(title=title, description=description, color=color)
        embed.set_thumbnail(
            url=interaction.guild.icon.url
            if interaction.guild.icon
            else disnake.Embed.Empty
        )
        if image:
            embed.set_image(url=image.url or disnake.Embed.Empty)

        view = AdminConfirm(interaction, embed, new=True)

        # check if welcome message exits
        if ext.get_welcome_message_id():
            # welcome message has not been sent previously
            view = AdminConfirm(interaction, embed, new=False)

        return await interaction.response.send_message(
            "Here is a preview of your Welcome message",
            embed=embed,
            view=view,
            ephemeral=True,
        )

    @commands.Cog.listener()
    async def on_button_click(self, interaction: disnake.MessageInteraction) -> None:
        button = interaction.component
        member = interaction.author

        if button.custom_id == "start_quiz":
            if member in ext.get_quizzed_members():
                return await interaction.response.send_message(
                    "You have already completed this quiz.", ephemeral=True
                )

            await interaction.response.defer()
            quiz = Quiz(interaction)
            await quiz.start()

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
