import sqlite3
import bcrypt
import pandas as pd
from .db import get_conn, initialize_schema
import os

DB_FILE = "DATA/intelligence_platform.db"
USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.txt')

def migrate():
     initialize_schema()
     if not os.path.exists(USERS_FILE):
         print('users.txt not found; create one with lines: username,password')
         return


with open(USERS_FILE, 'r', encoding='utf-8') as f:
     lines = [l.strip() for l in f if l.strip()]


with get_conn() as conn:
     cur = conn.cursor()
     for line in lines:
          try:
             username, password = [p.strip() for p in line.split(',')[:2]]
          except Exception:
             print('skipping malformed line:', line)
             continue
          pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
          try:
             cur.execute('INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)',
                        (username, pw_hash, __import__('datetime').datetime.utcnow().isoformat()))
             print(f'Inserted user: {username}')
          except Exception as e:
             print('could not insert', username, e)

def migrate_users():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    with open("DATA/users.txt", "r") as f:
        for line in f:
            username, password = line.strip().split(",")
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            try:
                cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed))
            except sqlite3.IntegrityError:
                pass
    conn.commit()
    conn.close()

def migrate_csv_to_table(csv_file, table_name, columns):
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(DB_FILE)
    df.to_sql(table_name, conn, if_exists="append", index=False)
    conn.close()

if __name__ == "__main__":
    migrate()
    migrate_users()
    migrate_csv_to_table("DATA/cyber_incidents.csv", "cyber_incidents", ["title","category","severity"])
    migrate_csv_to_table("DATA/datasets_metadata.csv", "datasets_metadata", ["name","rows","cols"])
    migrate_csv_to_table("DATA/it_tickets.csv", "it_tickets", ["requester","status","steps"])
    print("Data migration complete!")
