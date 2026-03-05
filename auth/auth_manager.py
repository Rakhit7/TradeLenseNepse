import json
import bcrypt

# Load user credentials from a JSON file
def load_users():
    try:
        with open("auth/users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user credentials to a JSON file
def save_user(username, password):
    users = load_users()
    if username in users:
        raise ValueError("Username already exists.")
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users[username] = hashed_password.decode()
    with open("auth/users.json", "w") as file:
        json.dump(users, file)

# Validate user credentials
def validate_user(username, password):
    users = load_users()
    if username in users and bcrypt.checkpw(password.encode(), users[username].encode()):
        return True
    return False

