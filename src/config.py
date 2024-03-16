import os

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv()

# todo: move it to env
DEFAULT_ICON_NAME = "default-icon.png"


class Settings(BaseSettings):
    main_db_url: PostgresDsn = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        path=f"/{os.getenv('POSTGRES_DB') or ''}",
    )
    sync_db_url: PostgresDsn = PostgresDsn.build(
        scheme="postgresql",
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        path=f"/{os.getenv('POSTGRES_DB') or ''}",
    )
    icons_path: str = os.getenv("SOURCES_ICONS_PATH")
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


global_settings = Settings()
