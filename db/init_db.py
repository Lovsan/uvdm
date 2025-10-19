"""
Database initialization and migration utilities for UVDM payment system.

This module provides functions to initialize the payment database schema
and run migrations. It uses SQLite as the default database.
"""

import os
import sqlite3
from datetime import datetime


# Default database path
DEFAULT_DB_PATH = os.path.join('data', 'payments.db')
MIGRATIONS_DIR = os.path.join('db', 'migrations')


def get_db_connection(db_path=None):
    """
    Get a database connection.
    
    Args:
        db_path: Path to the SQLite database file. Uses DEFAULT_DB_PATH if not provided.
        
    Returns:
        sqlite3.Connection: Database connection object
    """
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def run_migrations(db_path=None):
    """
    Run all SQL migration files from the migrations directory.
    
    Args:
        db_path: Path to the SQLite database file. Uses DEFAULT_DB_PATH if not provided.
        
    Returns:
        bool: True if migrations ran successfully, False otherwise
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        # Get list of migration files
        migration_files = sorted([
            f for f in os.listdir(MIGRATIONS_DIR)
            if f.endswith('.sql')
        ])
        
        if not migration_files:
            print("No migration files found.")
            return True
        
        print(f"Running {len(migration_files)} migration(s)...")
        
        for migration_file in migration_files:
            migration_path = os.path.join(MIGRATIONS_DIR, migration_file)
            print(f"  Running: {migration_file}")
            
            with open(migration_path, 'r', encoding='utf-8') as f:
                migration_sql = f.read()
            
            # Execute the migration
            cursor.executescript(migration_sql)
        
        conn.commit()
        conn.close()
        
        print("✓ All migrations completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        return False


def init_database(db_path=None):
    """
    Initialize the payment database with schema and seed data.
    
    Args:
        db_path: Path to the SQLite database file. Uses DEFAULT_DB_PATH if not provided.
        
    Returns:
        bool: True if initialization was successful, False otherwise
    """
    print("Initializing UVDM payment database...")
    return run_migrations(db_path)


if __name__ == '__main__':
    """Run migrations when this script is executed directly."""
    import sys
    
    db_path = None
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    
    success = init_database(db_path)
    sys.exit(0 if success else 1)
