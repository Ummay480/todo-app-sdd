#!/usr/bin/env python3
"""
Script to create/update the database schema
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database import engine, init_db
from src.models.user import User
from src.models.task import Task  # Import all models to register them
from sqlmodel import SQLModel
from sqlalchemy import text

def recreate_schema():
    print("Recreating database schema...")

    # Drop all tables and recreate them
    SQLModel.metadata.drop_all(engine)
    print("Dropped all tables")

    # Create all tables
    SQLModel.metadata.create_all(engine)
    print("Created all tables")

    # Verify the user table structure
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'user'
            ORDER BY ordinal_position;
        """))
        print("\nUser table structure:")
        for row in result:
            print(f"  {row[0]}: {row[1]}")

if __name__ == "__main__":
    recreate_schema()