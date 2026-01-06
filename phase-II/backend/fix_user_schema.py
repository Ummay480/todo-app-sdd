#!/usr/bin/env python3
"""
Script to check and fix the user table schema
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database import engine
from sqlalchemy import text

def check_and_fix_user_schema():
    print("Checking user table schema...")

    with engine.connect() as conn:
        # Check if the hashed_password column exists
        result = conn.execute(text("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'user' AND column_name = 'hashed_password';
        """))

        columns = list(result.fetchall())
        if len(columns) == 0:
            print("Adding missing 'hashed_password' column to user table...")
            conn.execute(text("ALTER TABLE \"user\" ADD COLUMN hashed_password VARCHAR;"))
            conn.commit()
            print("Column added successfully!")
        else:
            print("Column 'hashed_password' already exists.")

        # Check all columns in the user table
        result = conn.execute(text("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'user'
            ORDER BY ordinal_position;
        """))

        print("\nCurrent user table structure:")
        for row in result:
            print(f"  {row[0]}: {row[1]}")

if __name__ == "__main__":
    check_and_fix_user_schema()