import os

from dotenv import load_dotenv


load_dotenv()

MAIN_DATABASE_URL = os.getenv("MAIN_DATABASE_URL")
SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")
