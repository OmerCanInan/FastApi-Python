import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_URL = os.environ["DATABASE_URL"].replace("postgresql://", "postgresql+psycopg://", 1)
engine = create_engine(DB_URL)