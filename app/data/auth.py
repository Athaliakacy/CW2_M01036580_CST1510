import bcrypt
import os

# File where users will be stored
USERS_FILE = os.path.join("DATA", "users.txt")

# password hashing

def hash_password(password):
    """Turn plain password into secure hashed password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


# VERIFY PASSWORD

def verify_password(password, hashed):
    """Check if a plain password matches the stored hash."""
    return bcrypt.checkpw(password.encode(), hashed)

# LOAD USERS

def load_users():
    """Load all users from users.txt as {username: hashedpassword}."""
    users = {}

    if not os.path.exists(USERS_FILE):
        return users

    with open(USERS_FILE, "r") as f:
        for line in f:
            username, hashed = line.strip().split(":")
            users[username] = hashed.encode()

    return users


# SAVE NEW USER

def save_user(username, password):
    """Save a new user with hashed password into users.txt."""
    hashed = hash_password(password)

    with open(USERS_FILE, "a") as f:
        f.write(f"{username}:{hashed.decode()}\n")


# LOGIN USER

def login(username, password):
    """Return True if login success, False if wrong."""
    users = load_users()

    if username not in users:
        return False

    stored_hash = users[username]

    return verify_password(password, stored_hash)

# Authenticate user
def authenticate(username, password):
    users = load_users()
    if username not in users:
        return False

    stored_hash = users[username]
    return bcrypt.checkpw(password.encode(), stored_hash)

#Register user
def register(username, password):
    users = load_users()
    if username in users:
        return False  # user exists already

    save_user(username, password)
    return True
