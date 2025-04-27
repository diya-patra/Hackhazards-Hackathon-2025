import json
import os

# For user-based personal chats
def save_user_message(email, message, is_bot=False):
    filepath = f"data/chats/{email}.json"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    chat_data = []
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            chat_data = json.load(file)

    chat_data.append({
        "sender": "bot" if is_bot else "user",
        "message": message
    })

    with open(filepath, "w") as file:
        json.dump(chat_data, file, indent=2)

def load_user_history(email):
    filepath = f"data/chats/{email}.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return json.load(file)
    return []

# For collaborative group chats
def save_group_message(group_name, sender_email, message):
    filepath = f"data/groups/{group_name}.json"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    chat_data = []
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            chat_data = json.load(file)

    chat_data.append({
        "email": sender_email,
        "message": message
    })

    with open(filepath, "w") as file:
        json.dump(chat_data, file, indent=2)

def load_group_history(group_name):
    filepath = f"data/groups/{group_name}.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return json.load(file)
    return []