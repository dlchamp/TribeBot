"""
MIT License

Copyright (c) 2022 DLCHAMP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import asyncio
import json

import disnake

from bot import ext
from bot.quiz.quiz import Quiz


def load_config():
    with open("./bot/data/config.json") as f:
        return json.load(f)


def dump_config(data):
    with open("./bot/data/config.json", "w") as f:
        json.dump(data, f)


def get_welcome_message() -> bool:
    data = load_config()
    return data["welcome_message_id"]


def update_message_sent(message_id: int) -> None:
    data = load_config()
    data["welcome_message_id"] = message_id
    dump_config(data)


def get_welcome_embed():
    with open("./bot/data/welcome_embed.json") as f:
        return json.load(f)


def get_quizzed_members():
    data = load_config()
    return data["quizzed"]


def add_quizzed_member(member_id: int) -> None:
    data = load_config()
    data["quizzed"].append(member_id)
    dump_config(data)


class StartQuiz(disnake.ui.View):
    """Starts a quiz from the welcome message"""

    def __init__(self) -> None:
        super().__init__(timeout=None)

    @disnake.ui.button(
        label="Get Started", style=disnake.ButtonStyle.primary, custom_id="start"
    )
    async def get_started(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ) -> None:
        """Button for starting a new quiz"""

        # start a new quiz if the user has not already participated
        author_id = interaction.author.id
        quizzed = ext.get_quizzed_members()
        if author_id in quizzed:
            # already participated
            return await interaction.response.send_message(
                "Hey! You already completed this quiz. 🤔",
                ephemeral=True,
            )

        await interaction.response.defer(with_message=True, ephemeral=True)
        await asyncio.sleep(1.5)
        quiz = Quiz(interaction)
        await quiz.start()
