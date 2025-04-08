import os
import pathlib
from dotenv import load_dotenv

ROOT_DIR = pathlib.Path(__file__)
load_dotenv(dotenv_path= ROOT_DIR / ".env")

bot_token = os.getenv("bot_token")