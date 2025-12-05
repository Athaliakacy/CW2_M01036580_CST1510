# CW2_M01036580_CST1510
# Week 7: Secure Authentication System
Student Name: [Athalia]
Student ID: [M01036580]
Course: CST1510 -CW2 - Multi-Domain Intelligence Platform
## Project Description
A command-line authentication system implementing secure password hashing
This system allows users to register accounts and log in with proper pass
## Features
- Secure password hashing using bcrypt with automatic salt generation
- User registration with duplicate username prevention
- User login with password verification
- Input validation for usernames and passwords
- File-based user data persistence
## Technical Implementation
- Hashing Algorithm: bcrypt with automatic salting
Data Storage: Plain text file (`users.txt`) with comma-separated values
- Password Security: One-way hashing, no plaintext storage
- Validation: Username (3-20 alphanumeric characters), Password (6-50 characters)
## Week8: Data Pipeline & CRUD (SQL)
## What this contains
- Database layer (`app/data/`)
- Business logic for migration & auth (`app/services/user_service.py`)
- CSV data files in `DATA/`
- SQLite DB created at `DATA/intelligence_platform.db`

## Quick start
1. Create and activate a virtual environment.
2. `pip install -r requirements.txt`
3. Initialize DB:
   `python main.py init`
4. Migrate Week 7 users and CSVs:
   `python main.py migrate`
5. (Optional) Run Streamlit UI in later weeks.

## Notes
- `DATA/users.txt` expected format: `username:password` per line.
- CSVs should have columns as described in the assignment.
