import os

from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
RESET_PWD_SECRET = os.getenv("RESET_PWD_SECRET")
VERIFICATION_TOKEN_SECRET = os.getenv("VERIFICATION_TOKEN_SECRET")
