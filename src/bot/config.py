"""
Contains all configuration data for the bot
"""
import os


class Config:

    # auth tokens for bot gateway
    bot_token = os.getenv("TOKEN")

    # base default role for new members assigned with
    # tribe role, Copy role ID and paste between ""
    default_role_id = ""

    # welcome channel ID
    # id for the channel where the bot will send the welcome message
    # that includes the button to start the quiz.
    # It wil only send once on first boot up if the message does not already exist
    welcome_channel_id = ""

    # twitter oauth url
    # this is the external url that will be attached to the quiz complete message
    twitter_oauth_url = "https://text.com"

    # configure this section for the tribes
    # add the ID for each tribes role by replacing the 0000s
    # you can also update the icon_url for each tribe so that the correct image is attached to the quiz complete embed
    tribes = {
        "Zuberi": {
            "role_id": 000000,
            "description": "Brave, astronomer/intellects, explorer, traveler, grounded, arrogant",
            "icon_url": "https://cdn.dribbble.com/users/789080/screenshots/4427574/mountain_tribe_icon.jpg",
            "summary": "This is a long summary describing this tribe",
        },
        "Panuk": {
            "role_id": 000000,
            "description": "Leadership, care, decision making, hunter/resourceful, seamstress, kind, reliant",
            "icon_url": "https://cdn.dribbble.com/users/789080/screenshots/4427574/mountain_tribe_icon.jpg",
            "summary": "This is a long summary describing this tribe",
        },
        "Briar": {
            "role_id": 000000,
            "description": "Chef, farmer, jolly, confident, funny, weak, hard worker, loyal, fair",
            "icon_url": "https://cdn.dribbble.com/users/789080/screenshots/4427574/mountain_tribe_icon.jpg",
            "summary": "This is a long summary describing this tribe",
        },
        "Mira": {
            "role_id": 000000,
            "description": "Clever/witty, curious, observant, fishers, ambitious, adventurous, sneaky",
            "icon_url": "https://cdn.dribbble.com/users/789080/screenshots/4427574/mountain_tribe_icon.jpg",
            "summary": "This is a long summary describing this tribe",
        },
    }
