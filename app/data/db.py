import sqlite3
from pathlib import Path

# Path to the DB file stored inside the DATA/ folder
DB_FOLDER = Path("DATA")
DB_PATH = DB_FOLDER / "intelligence_platform.db"


def connect_database(db_path=DB_PATH):
    """
    Connect to SQLite database.
    Automatically creates the DATA folder if it doesn't exist.
    Returns a connection object.
    """

    # Ensure the DATA folder exists
    DB_FOLDER.mkdir(parents=True, exist_ok=True)

    # Connect to database
    conn = sqlite3.connect(str(db_path))

    # Return connection
    return conn
