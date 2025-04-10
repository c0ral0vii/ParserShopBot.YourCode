### This file contains the configuration for the bot.
import os
import pathlib
from dotenv import load_dotenv

ROOT_DIR = pathlib.Path(__file__)
load_dotenv()

bot_token = os.getenv("bot_token")
FOREX_API = os.getenv("FOREX_API")