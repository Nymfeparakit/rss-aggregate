import os

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv()


class Settings(BaseSettings):
    main_db_url: PostgresDsn = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port="5432",
        path=f"/{os.getenv('POSTGRES_DB') or ''}",
    )
    sync_db_url: PostgresDsn = PostgresDsn.build(
        scheme="postgresql",
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port="5432",
        path=f"/{os.getenv('POSTGRES_DB') or ''}",
    )


global_settings = Settings()
