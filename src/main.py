from bot import Config, bot, send_welcome_message


def main(bot):
    """Run the bot"""
    send_welcome_message.start()
    bot.run(Config.bot_token)


if __name__ == "__main__":
    main(bot)
