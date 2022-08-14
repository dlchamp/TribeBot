"""
Contains all configuration data for the bot
"""


class Config:

    # auth tokens for bot gateway
    bot_token: str = ""

    # base default role for new members assigned with
    # tribe role, Copy role ID and paste between ""
    default_role_id = ""

    # tribe roles
    tribe_z_role_id = ""
    tribe_p_role_id = ""
    tribe_b_role_id = ""
    tribe_m_role_id = ""

    # welcome channel ID
    # id for the channel where the bot will send the welcome message
    # that includes the button to start the quiz.
    # It wil only send once on first boot up if the message does not already exist
    welcome_channel_id = ""
