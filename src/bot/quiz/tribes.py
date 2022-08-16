"""Handle the Tribe classes"""
from dataclasses import dataclass

from disnake import Role


@dataclass
class Tribe:
    """Represents a Tribe"""

    name: str
    description: str
    icon_url: str
    role: Role
