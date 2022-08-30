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
import random

import disnake
from bot import ext
from bot.config import Config
from bot.quiz.tribes import Tribe


class Quiz:
    """Handles the quiz questions and answers"""

    def __init__(self, interaction: disnake.MessageInteraction) -> None:
        self.interaction = interaction
        self.quiz = self.get_quiz()
        self.answers = {}

    async def start(self):
        """start the quiz"""

        interaction = self.interaction
        author = interaction.author
        guild = interaction.guild
        bot = interaction.bot
        response = None

        # shuffle quiz questions
        random.shuffle(self.quiz)

        for i, quiz_item in enumerate(self.quiz, 1):

            question = quiz_item["question"]
            answers = quiz_item["answers"]

            # shuffle the answers each question
            random.shuffle(answers)

            # build the question embed
            embed = disnake.Embed(
                title="Find your Tribe!", description=f"Question {i}/{len(self.quiz)}"
            )
            embed.add_field(name="Question:", value=question)
            embed.add_field(
                name="Answers:",
                value=f"**A** - {answers[0].split('-')[1]}\n"
                f"**B** - {answers[1].split('-')[1].strip()}\n"
                f"**C** - {answers[2].split('-')[1].strip()}\n"
                f"**D** - {answers[3].split('-')[1].strip()}",
                inline=False,
            )
            embed.set_thumbnail(
                url=guild.icon.url if guild.icon else disnake.Embed.Empty
            )

            # create the answer buttons for the embedded quiz question
            view = self.create_view(answers)

            # if it's the first question, respond to the interaction with a followup
            # if it's not the first, update the question/answers for subsequent questions
            if i == 1:
                # first question
                await interaction.followup.send(embed=embed, ephemeral=True, view=view)
            else:
                await response.response.edit_message(embed=embed, view=view)

            # handle the button clicks
            try:
                button_response = await bot.wait_for(
                    "button_click",
                    check=lambda i: i.author == interaction.author,
                    timeout=120,
                )
                response = button_response

            except asyncio.TimeoutError:
                # button wasn't clicked fast enough or the ephemeral message was closed
                if str(author.id) in self.answers:
                    del self.answers[str(author.id)]

                return await response.response.edit_message(
                    content="You took too long to respond. Please answer each question within the 2 minute time limit.",
                    embed=None,
                    view=view.clear_items(),
                )

            # add the selected answer for later calculations
            tribe = response.component.custom_id
            self.add_answer(author, tribe)

        # quiz finished - calculate and add roles
        tribe = self.calculate_results(author, guild)
        default_role = guild.get_role(int(Config.default_role_id))

        # add roles to user
        await self.add_roles(author, [tribe.role, default_role])

        # send final message with calculated tribe and external link for twitter oauth
        # to send tweet about your new tribe
        embed = self.create_complete_quiz_embed(tribe)

        await response.response.edit_message(
            embed=embed,
            components=[
                disnake.ui.Button(
                    label="Share on Twitter!", url=Config.twitter_oauth_url
                )
            ],
        )

        # add member to quizzed
        ext.add_quizzed_member(author.id)

    def create_complete_quiz_embed(self, tribe: Tribe) -> disnake.Embed:
        """Creates the embed for when the quiz is completed"""
        embed = disnake.Embed(
            title=f"Welcome to the {tribe.name} Tribe!",
            description=f"{tribe.summary}\n\nMembers of the **{tribe.name}** tribe are found to be:\n> {tribe.description}",
        )
        embed.set_thumbnail(url=tribe.icon_url)
        embed.set_footer(
            text="Tweet about your new tribe by following the button below!"
        )
        return embed

    def create_view(self, answers: list[str]) -> disnake.ui.View:
        """Create the view and add answer buttons = Returns a created view"""
        view = disnake.ui.View()
        view.add_item(
            disnake.ui.Button(
                label="A",
                style=disnake.ButtonStyle.primary,
                custom_id=answers[0].split("-")[0].strip(),
            )
        )
        view.add_item(
            disnake.ui.Button(
                label="B",
                style=disnake.ButtonStyle.primary,
                custom_id=answers[1].split("-")[0].strip(),
            )
        )
        view.add_item(
            disnake.ui.Button(
                label="C",
                style=disnake.ButtonStyle.primary,
                custom_id=answers[2].split("-")[0].strip(),
            )
        )
        view.add_item(
            disnake.ui.Button(
                label="D",
                style=disnake.ButtonStyle.primary,
                custom_id=answers[3].split("-")[0].strip(),
            )
        )

        return view

    async def add_roles(
        self, author: disnake.Member, roles: list[disnake.Role]
    ) -> None:
        """add roles to member"""
        await author.add_roles(*roles, reason="Completed Quiz")

    def get_quiz(self) -> None:
        """Get the quiz and load the questions answers"""
        with open("./bot/data/quiz.json") as f:
            return json.load(f)

    def add_answer(self, author: disnake.Member, value: str) -> None:
        """Add the answer and count for each tribe"""
        author_id = str(author.id)

        if value == "start":
            return

        if not author_id in self.answers:
            self.answers[author_id] = {}

        if not value in self.answers[author_id]:
            self.answers[author_id][value] = 0

        self.answers[author_id][value] += 1

    def calculate_results(self, author: disnake.Member, guild: disnake.Guild) -> Tribe:
        """Calculate the answers and find the most answers that correlates
        with a tribe"""
        author_id = str(author.id)
        answers = self.answers[author_id]
        sorted_answers = sorted(answers.items(), key=lambda a: a[1], reverse=True)
        top_tribe = sorted_answers[0][0]

        # del answers after sorting and calculating
        del answers

        return Tribe(
            name=top_tribe,
            description=Config.tribes[top_tribe]["description"],
            summary=Config.tribes[top_tribe]["summary"],
            icon_url=Config.tribes[top_tribe]["icon_url"],
            role=guild.get_role(int(Config.tribes[top_tribe]["role_id"])),
        )
