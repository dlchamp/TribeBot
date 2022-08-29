"""
Contains all configuration data for the bot
"""


class Config:

    # auth tokens for bot gateway
    bot_token = "MTAxMzUxNjEzODEzNjczNTk0NA.G6qjlw.DSJ2f8yW9xTTlc2w5_QvIvsTsZBv_ZkVimG63U"

    # base default role for new members assigned with
    # tribe role, Copy role ID and paste between ""
    default_role_id = "1013571298749841418"

    # configure this section for the tribes
    # add the ID for each tribes role by replacing the 0000s
    # you can also update the icon_url for each tribe so that the correct image is attached to the quiz complete embed
    tribes = {
        "Z": {
            "role_id": 1013571968731201627,
            "description": "Brave, astronomer/intellects, explorer, traveler, grounded & arrogant",
            "icon_url": "https://cdn.dribbble.com/users/789080/screenshots/4427574/mountain_tribe_icon.jpg",
        },
        "P": {
            "role_id": 1013572038545391716,
            "description": "Leadership, care, decision making, hunter/resourceful, seamstress, kind & reliant",
            "icon_url": "https://cdn.dribbble.com/users/789080/screenshots/4427574/mountain_tribe_icon.jpg",
        },
        "B": {
            "role_id": 1013572070388543628,
            "description": "Chef, farmer, jolly, confident, funny, weak, hard worker, loyal & fair",
            "icon_url": "https://cdn.dribbble.com/users/789080/screenshots/4427574/mountain_tribe_icon.jpg",
        },
        "M": {
            "role_id": 1013572109185855688,
            "description": "Clever/witty, curious, observant, fishers, ambitious, adventurous & sneaky",
            "icon_url": "https://cdn.dribbble.com/users/789080/screenshots/4427574/mountain_tribe_icon.jpg",
        },
    }

    # welcome channel ID
    # id for the channel where the bot will send the welcome message
    # that includes the button to start the quiz.
    # It wil only send once on first boot up if the message does not already exist
    welcome_channel_id = "1013516771224985663"

    # twitter oauth url
    # this is the external url that will be attached to the quiz complete message
    twitter_oauth_url = "https://twitter.com/avgnomad"
