import sqlalchemy
from sqlalchemy import create_engine, text
import sys

from app.core.config import settings
from app.db.init_db import init_db
import asyncio
import logging

# Configure basic logging to see output
logging.basicConfig(level=logging.INFO)

async def run_init():
    print(f"Initializing database at: {settings.DATABASE_URL}")
    try:
        await init_db()
        print("Database initialization successful!")
    except Exception as e:
        print(f"Error during initialization: {e}")

if __name__ == "__main__":
    asyncio.run(run_init())
