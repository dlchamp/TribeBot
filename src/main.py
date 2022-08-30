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
import os

from dotenv import load_dotenv
from loguru import logger

load_dotenv("token.env")

from bot import bot
from bot.config import Config


def main(bot) -> None:
    """Bot.run is a blocking method, code defined
    after will not run until bot is stopped"""
    bot.run(Config.bot_token)


def check_config() -> bool:
    """Check that all variables in config file have been set (are not empty "")"""

    failed = 0

    if Config.bot_token is None:
        failed += 1
        logger.critical("Bot token was not found")

    if Config.default_role_id == "":
        failed += 1
        logger.critical("Default Role ID was not found in config.py")

    if Config.welcome_channel_id == "":
        failed += 1
        logger.critical("Welcome channel ID was not found in config.py")

    if Config.twitter_oauth_url == "":
        failed += 1
        logger.critical("Twitter oauth url was not found in config.py")

    return failed == 0


if __name__ == "__main__":

    # run pre-check
    if check_config():
        logger.success("Pre-run config check passed - Starting bot...")
        main(bot)

    else:
        logger.warning("Pre-run config check failed - Exiting...")
