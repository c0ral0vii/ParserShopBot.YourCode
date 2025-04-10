### This file contains the configuration for the bot.
import os
import pathlib
from dotenv import load_dotenv

ROOT_DIR = pathlib.Path(__file__)
load_dotenv(".env")

bot_token = os.getenv("bot_token")