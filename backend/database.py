import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Reads the .env file and loads DATABASE_URL into the environment
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# The "engine" is the actual connection to your Postgres database
engine = create_engine(DATABASE_URL)

# SessionLocal will let us create a new "conversation" with the database
# for each request that needs one
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is what all our table classes will inherit from
Base = declarative_base()