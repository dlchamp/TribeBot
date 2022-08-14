"""Handles all of the quiz details, answer selection, and role assignment"""

import asyncio
import json
import random

import disnake
from bot import ext
from bot.config import Config
from bot.quiz.tribes import Tribe, tribes


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
                f"**B** - {answers[1].split('-')[1]}\n"
                f"**C** - {answers[2].split('-')[1]}\n"
                f"**D** - {answers[3].split('-')[1]}",
                inline=False,
            )

            # ask the question and place the buttons for answer selection
            view = disnake.ui.View()
            view.add_item(
                disnake.ui.Button(
                    label="A",
                    style=disnake.ButtonStyle.primary,
                    custom_id=answers[0].split("-")[0],
                )
            )
            view.add_item(
                disnake.ui.Button(
                    label="B",
                    style=disnake.ButtonStyle.primary,
                    custom_id=answers[1].split("-")[0],
                )
            )
            view.add_item(
                disnake.ui.Button(
                    label="C",
                    style=disnake.ButtonStyle.primary,
                    custom_id=answers[2].split("-")[0],
                )
            )
            view.add_item(
                disnake.ui.Button(
                    label="D",
                    style=disnake.ButtonStyle.primary,
                    custom_id=answers[3].split("-")[0],
                )
            )

            if i == 1:
                # first question
                await interaction.followup.send(embed=embed, ephemeral=True, view=view)
            else:
                await response.response.edit_message(embed=embed, view=view)

            try:
                button_response = await bot.wait_for(
                    "button_click",
                    check=lambda i: i.author == interaction.author,
                    timeout=120,
                )
                response = button_response

            except asyncio.TimeoutError:
                if str(author.id) in self.answers:
                    del self.answers[str(author.id)]

                return await interaction.edit_original_message(
                    content="You took too long to respond. Please answer each question within the 2 minute time limit.",
                    embed=None,
                    view=view.clear_items(),
                )

            tribe = response.component.custom_id
            self.add_answer(author, tribe)

        # quiz finished - calculate and add roles
        tribe = self.calculate_results(author, guild)
        default_role = guild.get_role(int(Config.default_role_id))

        # add roles to user
        await self.add_roles(author, [tribe.role, default_role])

        await interaction.edit_original_message(
            content=f"You completed the quiz!\nI calculated that you belong in the **{tribe.name} tribe** because you are **{tribe.description}**.",
            embed=None,
            view=None,
        )

        # add member to quizzed
        ext.add_quizzed_member(author.id)

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
            description=tribes[top_tribe]["description"],
            role=guild.get_role(int(tribes[top_tribe]["role_id"])),
        )
