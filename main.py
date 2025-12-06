from app.data.schema import create_all_tables
from app.services.user_services import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents
import os
from app.data.db import connect_database
def main():
    print("=" * 65)
    print(" WEEK 8 – INTELLIGENCE PLATFORM DATABASE DEMO")
    print("=" * 65)

    # 1. Ensure DATA folder exists
    if not os.path.exists("DATA"):
        os.makedirs("DATA")
        print("[INFO] DATA folder created.")
    else:
        print("[INFO] DATA folder already exists.")

    # 2. Create Database + All Tables
    print("\n[STEP] Creating / verifying database tables...")
    conn = connect_database()
    create_all_tables(conn)
    conn.close()
    print("[OK] All tables created successfully.")

    # 3. Migrate users from users.txt
    print("\n[STEP] Migrating users from text file...")
    try:
        migrate_users_from_file()
        print("[OK] User migration complete.")
    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")

    # 4. Test Registration & Login
    print("\n[STEP] Testing authentication logic...")
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(f"Register: {msg}")

    success, msg = login_user("alice", "SecurePass123!")
    print(f"Login: {msg}")

    # 5. Test inserting an incident
    print("\n[STEP] Testing Cyber Incident CRUD...")
    try:
        incident_id = insert_incident(
            "2024-11-05",          # date
            "Phishing",            # category
            "High",                # severity
            "Open",                # status
            "Suspicious email detected",
            "alice"                # reporter
        )
        print(f"[OK] Incident #{incident_id} created successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to create incident: {e}")

    # 6. Test reading all incidents into pandas DataFrame
    print("\n[STEP] Checking database contents...")
    try:
        df = get_all_incidents()
        print(df)
        print(f"Total incidents: {len(df)}")
    except Exception as e:
        print(f"[ERROR] Cannot load incidents: {e}")

    print("\n[COMPLETE] Program finished successfully!")
    print("=" * 65)
