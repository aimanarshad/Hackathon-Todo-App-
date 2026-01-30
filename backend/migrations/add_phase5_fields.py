"""Migration script to add Phase 5 fields to existing Task table."""
import sys
import os

# Add the backend directory to the path so we can import models
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import Column, DateTime, Boolean, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from backend.database import DATABASE_URL
from backend.models import Task, engine


def add_phase5_fields():
    """Add Phase 5 fields to the Task table."""
    print("Starting migration to add Phase 5 fields...")

    # Connect to the database
    with engine.connect() as conn:
        # Check if columns already exist to avoid errors
        existing_columns = []
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'task'
        """))

        for row in result:
            existing_columns.append(row[0])

        # Add Phase 5 fields if they don't exist
        if 'due_date' not in existing_columns:
            print("Adding due_date column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN due_date TIMESTAMP WITH TIME ZONE"))
            conn.commit()

        if 'reminder_enabled' not in existing_columns:
            print("Adding reminder_enabled column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN reminder_enabled BOOLEAN DEFAULT FALSE"))
            conn.commit()

        if 'reminder_time' not in existing_columns:
            print("Adding reminder_time column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN reminder_time TIMESTAMP WITH TIME ZONE"))
            conn.commit()

        if 'recurrence_pattern' not in existing_columns:
            print("Adding recurrence_pattern column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN recurrence_pattern VARCHAR"))
            conn.commit()

        if 'recurrence_interval' not in existing_columns:
            print("Adding recurrence_interval column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN recurrence_interval INTEGER DEFAULT 1"))
            conn.commit()

        if 'recurrence_end_date' not in existing_columns:
            print("Adding recurrence_end_date column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN recurrence_end_date TIMESTAMP WITH TIME ZONE"))
            conn.commit()

        if 'recurrence_parent_id' not in existing_columns:
            print("Adding recurrence_parent_id column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN recurrence_parent_id INTEGER"))
            conn.commit()

        if 'recurrence_next_instance' not in existing_columns:
            print("Adding recurrence_next_instance column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN recurrence_next_instance TIMESTAMP WITH TIME ZONE"))
            conn.commit()

        if 'is_recurring_template' not in existing_columns:
            print("Adding is_recurring_template column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN is_recurring_template BOOLEAN DEFAULT FALSE"))
            conn.commit()

        if 'timezone' not in existing_columns:
            print("Adding timezone column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN timezone VARCHAR DEFAULT 'UTC'"))
            conn.commit()

    print("Migration completed successfully!")


if __name__ == "__main__":
    add_phase5_fields()