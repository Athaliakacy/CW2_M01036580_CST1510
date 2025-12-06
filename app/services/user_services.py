import os
import bcrypt
import pandas as pd
from app.data import db, users as users_dao, incidents as incidents_dao, datasets as datasets_dao, tickets as tickets_dao
from app.data.schema import init_db,create_users_table
from app.data.users import get_user_by_username

DATA_USERS_TXT = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")), "DATA", "users.txt")
DATA_DIR = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")), "DATA")

def login_user(username, password):
    """Authenticate user."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."
    
    # Verify password
    stored_hash = user[2]  # password_hash column
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, f"Login successful!"
    return False, "Incorrect password."

def migrate_users_from_file(filepath='DATA/users.txt'):
    """Migrate users from text file to database."""
    # migration logic 

def initialize_platform():
    """
    Initialize DB schema and ensure DATA folder exists.
    """
    init_db()

def hash_password(plain_password: str) -> bytes:
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())

def migrate_users_txt_to_db(users_txt_path: str = DATA_USERS_TXT):
    """
    Read DATA/users.txt lines of form username:plaintextpassword or username:hashed
    For safety we expect plaintext for migration; if hashed, this will still be stored as is.
    This function will create users in DB with hashed passwords.
    """
    if not os.path.exists(users_txt_path):
        print("No users.txt found to migrate.")
        return

    with open(users_txt_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # allow two formats: username:password OR username:hashedstring (we'll treat as plaintext and re-hash)
            try:
                username, password = line.split(":", 1)
            except ValueError:
                continue
            # hash plaintext password
            try:
                hashed = hash_password(password)
                users_dao.create_user(username, hashed)
            except Exception as e:
                # skip duplicates or bad entries
                print(f"Skipping user {username}: {e}")

def migrate_csvs_to_db():
    """
    Loads CSVs from DATA/ into tables using pandas.
    Each CSV should have matching columns:
      - cyber_incidents.csv => title,category,severity
      - datasets_metadata.csv => name,rows,cols
      - it_tickets.csv => requester,assigned_to,status,steps
    This appends rows; run once.
    """
    # Incidents
    incidents_csv = os.path.join(DATA_DIR, "cyber_incidents.csv")
    if os.path.exists(incidents_csv):
        try:
            df = pd.read_csv(incidents_csv)
            for _, r in df.iterrows():
                title = str(r.get("title", "")).strip()
                category = str(r.get("category", "")).strip()
                severity = int(r.get("severity", 1))
                incidents_dao.add_incident(title, category, severity)
        except Exception as e:
            print("Error migrating incidents:", e)

    # Datasets
    datasets_csv = os.path.join(DATA_DIR, "datasets_metadata.csv")
    if os.path.exists(datasets_csv):
        try:
            df = pd.read_csv(datasets_csv)
            for _, r in df.iterrows():
                name = str(r.get("name", "")).strip()
                rows = int(r.get("rows", 0))
                cols = int(r.get("cols", 0))
                datasets_dao.add_dataset(name, rows, cols)
        except Exception as e:
            print("Error migrating datasets:", e)

    # Tickets
    tickets_csv = os.path.join(DATA_DIR, "it_tickets.csv")
    if os.path.exists(tickets_csv):
        try:
            df = pd.read_csv(tickets_csv)
            for _, r in df.iterrows():
                requester = str(r.get("requester", "")).strip()
                assigned_to = str(r.get("assigned_to", "")).strip() if "assigned_to" in r else None
                status = str(r.get("status", "open")).strip()
                steps = int(r.get("steps", 1))
                tickets_dao.add_ticket(requester, assigned_to, status, steps)
        except Exception as e:
            print("Error migrating tickets:", e)

def register_user(username: str, password: str) -> bool:
    """
    Register a new user into DB. Returns True if created, False if exists.
    """
    hashed = hash_password(password)
    return users_dao.create_user(username, hashed)

def authenticate_user(username: str, password: str) -> bool:
    """
    Verify login against DB stored bcrypt hash.
    """
    user = users_dao.get_user_by_username(username)
    if not user:
        return False
    stored_hash = user["password_hash"]
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode()  # in case stored as text
    return bcrypt.checkpw(password.encode(), stored_hash)
