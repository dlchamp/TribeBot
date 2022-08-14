"""Handle the Tribe classes"""
from dataclasses import dataclass

import disnake
from bot.config import Config

tribes = {
    "Z": {
        "role_id": Config.tribe_z_role_id,
        "description": "Brave, astronomer/intellects, explorer, traveler, grounded, arrogant",
    },
    "P": {
        "role_id": Config.tribe_p_role_id,
        "description": "Leadership, care, decision making, hunter/resourceful, seamstress, kind, reliant",
    },
    "B": {
        "role_id": Config.tribe_b_role_id,
        "description": "Chef, farmer, jolly, confident, funny, weak, hard worker, loyal, fair",
    },
    "M": {
        "role_id": Config.tribe_m_role_id,
        "description": "Clever/witty, curious, observant, fishers, ambitious, adventurous, sneaky",
    },
}


@dataclass
class Tribe:
    """Represents a Tribe"""

    name: str
    description: str
    role: disnake.Role
