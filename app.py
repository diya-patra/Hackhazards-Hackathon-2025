# from flask import Flask, request, jsonify, render_template, redirect, url_for, session
# import json
# import os
# import uuid
# import datetime
# import requests

# app = Flask(__name__)
# app.secret_key = "your_secret_key"

# USERS_FILE = "users.json"
# CHAT_HISTORY_FILE = "chat_history.json"
# GROUPS_FILE = "chat_groups.json"

# # ========================= UTILS =========================

# def load_json(filename):
#     if not os.path.exists(filename):
#         with open(filename, 'w') as f:
#             json.dump({}, f)
#     with open(filename, 'r') as f:
#         return json.load(f)

# def save_json(filename, data):
#     with open(filename, 'w') as f:
#         json.dump(data, f, indent=4)

# # ========================= ROUTES =========================

# @app.route('/')
# def home():
#     if 'username' in session:
#         return redirect(url_for('dashboard'))
#     return redirect(url_for('login'))

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']

#         users = load_json(USERS_FILE)
#         if username in users:
#             return "Username already exists. Try another."

#         users[username] = {'email': email, 'password': password}
#         save_json(USERS_FILE, users)
#         return redirect(url_for('login'))

#     return render_template('signup.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')

#         users = load_json(USERS_FILE)
#         #if user['username'] == username and user['password'] == password:
#         if username in users and users[username]['password'] == password:
#             session['username'] = username
#             return redirect(url_for('dashboard'))

#         return "Invalid credentials. Please try again."

#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('login'))

# @app.route('/dashboard')
# def dashboard():
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     groups = load_json(GROUPS_FILE)
#     user_groups = [name for name, data in groups.items() if session['username'] in data['members']]
#     return render_template('dashboard.html', username=session['username'], user_groups=user_groups)

# # ========================= PRIVATE CHAT =========================

# @app.route('/private_chat')
# def private_chat():
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     username = session['username']
#     chat_history = load_json(CHAT_HISTORY_FILE)
#     user_history = chat_history.get(username, [])
#     return render_template('private_chat.html', username=username, chat_history=user_history)

# @app.route('/send_private_message', methods=['POST'])
# def send_private_message():
#     if 'username' not in session:
#         return jsonify({'error': 'Not logged in'}), 401

#     user = session['username']
#     user_input = request.json['message']
#     chat_history = load_json(CHAT_HISTORY_FILE)

#     bot_response = generate_bot_response(user_input)

#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     entry_user = {"sender": user, "message": user_input, "timestamp": timestamp}
#     entry_bot = {"sender": "bot", "message": bot_response, "timestamp": timestamp}

#     chat_history.setdefault(user, []).extend([entry_user, entry_bot])
#     save_json(CHAT_HISTORY_FILE, chat_history)

#     return jsonify({"response": bot_response})

# # ========================= GROUP CHAT =========================

# @app.route('/group_chat/<group_name>')
# def group_chat(group_name):
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     groups = load_json(GROUPS_FILE)
#     if group_name not in groups or session['username'] not in groups[group_name]['members']:
#         return "Access denied."

#     chat_history = load_json(CHAT_HISTORY_FILE)
#     group_history = chat_history.get(group_name, [])

#     return render_template('group_chat.html', group_name=group_name, username=session['username'], chat_history=group_history)

# @app.route('/send_group_message/<group_name>', methods=['POST'])
# def send_group_message(group_name):
#     if 'username' not in session:
#         return jsonify({'error': 'Not logged in'}), 401

#     groups = load_json(GROUPS_FILE)
#     if group_name not in groups or session['username'] not in groups[group_name]['members']:
#         return jsonify({'error': 'Not a group member'}), 403

#     user = session['username']
#     user_input = request.json['message']
#     chat_history = load_json(CHAT_HISTORY_FILE)

#     bot_response = generate_bot_response(user_input)

#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     entry_user = {"sender": user, "message": user_input, "timestamp": timestamp}
#     entry_bot = {"sender": "bot", "message": bot_response, "timestamp": timestamp}

#     chat_history.setdefault(group_name, []).extend([entry_user, entry_bot])
#     save_json(CHAT_HISTORY_FILE, chat_history)

#     return jsonify({"response": bot_response})

# # ========================= GROUP CREATION =========================

# @app.route('/create_group', methods=['GET', 'POST'])
# def create_group():
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         group_name = request.form['group_name']
#         emails = request.form['emails'].split(',')

#         groups = load_json(GROUPS_FILE)
#         if group_name in groups:
#             return "Group name already exists."

#         users = load_json(USERS_FILE)
#         invited = [session['username']]

#         for username, data in users.items():
#             if data['email'] in emails:
#                 invited.append(username)

#         groups[group_name] = {'members': invited}
#         save_json(GROUPS_FILE, groups)

#         return redirect(url_for('dashboard'))

#     return render_template('create_group.html')

# # ========================= BOT LOGIC =========================

# def generate_bot_response(user_input):
#     groq_api_key = os.getenv("GROQ_API_KEY")
#     if not groq_api_key:
#         return "Groq API key is not configured."

#     url = "https://api.groq.com/openai/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {groq_api_key}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "model": "mixtral-8x7b-32768",
#         "messages": [{"role": "user", "content": user_input}],
#         "temperature": 0.7
#     }

#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         result = response.json()
#         return result['choices'][0]['message']['content'].strip()
#     except Exception as e:
#         return f"Error: {str(e)}"

# # ========================= MAIN =========================

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from groq_api import ask_groq  # Import ask_groq from your groq_api.py

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change to a strong secret key

# Load chat history or initialize if not exist
if os.path.exists('chat_history.json'):
    with open('chat_history.json', 'r') as f:
        chat_history = json.load(f)
else:
    chat_history = {
        "private_chats": {},
        "user_ai_chats": {},
        "group_chats": {}
    }

# Load users or initialize if not exist
if os.path.exists('users.json'):
    with open('users.json', 'r') as f:
        users = json.load(f)
else:
    users = {}

# Save chat history
def save_chat_history():
    with open('chat_history.json', 'w') as f:
        json.dump(chat_history, f, indent=4)

# Save users
def save_users():
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if username in users:
            return 'Username already exists. Please choose a different one.'

        users[username] = {
            'email': email,
            'password': password
        }
        save_users()
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password.'

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    # Prepare chat summaries
    private_chats = []
    if username in chat_history['private_chats']:
        private_chats = list(chat_history['private_chats'][username].keys())

    group_chats = list(chat_history['group_chats'].keys())

    return render_template('dashboard.html', username=username, private_chats=private_chats, group_chats=group_chats)

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if username not in chat_history['user_ai_chats']:
        chat_history['user_ai_chats'][username] = []

    if request.method == 'POST':
        message = request.form['message']
        if message:
            chat_history['user_ai_chats'][username].append({'sender': username, 'text': message})
            # AI response from Groq
            ai_response = ask_groq(message)
            chat_history['user_ai_chats'][username].append({'sender': 'AI', 'text': ai_response})
            save_chat_history()

    messages = chat_history['user_ai_chats'][username]
    return render_template('chatbot.html', username=username, messages=messages)

@app.route('/private_chat', methods=['GET', 'POST'])
def private_chat():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    users_list = list(users.keys())

    selected_user = request.form.get('receiver') or request.args.get('receiver') or users_list[0]

    if username not in chat_history['private_chats']:
        chat_history['private_chats'][username] = {}
    if selected_user not in chat_history['private_chats'][username]:
        chat_history['private_chats'][username][selected_user] = []

    if request.method == 'POST':
        message = request.form['message']
        if message:
            chat_history['private_chats'][username][selected_user].append({'sender': username, 'text': message})
            # Also save to the receiver's history
            if selected_user not in chat_history['private_chats']:
                chat_history['private_chats'][selected_user] = {}
            if username not in chat_history['private_chats'][selected_user]:
                chat_history['private_chats'][selected_user][username] = []
            chat_history['private_chats'][selected_user][username].append({'sender': username, 'text': message})
            save_chat_history()

    messages = chat_history['private_chats'][username][selected_user]

    return render_template('private_chat.html', username=username, users=users_list, selected_user=selected_user, messages=messages)

@app.route('/group_chat/<group_name>', methods=['GET', 'POST'])
def group_chat(group_name):
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if group_name not in chat_history['group_chats']:
        chat_history['group_chats'][group_name] = []

    if request.method == 'POST':
        message = request.form['message']
        if message:
            chat_history['group_chats'][group_name].append({'sender': username, 'text': message})
            # AI response from Groq for group chat
            ai_response = ask_groq(message)
            chat_history['group_chats'][group_name].append({'sender': 'AI', 'text': ai_response})
            save_chat_history()

    messages = chat_history['group_chats'][group_name]

    return render_template('group_chat.html', username=username, group_name=group_name, messages=messages)

@app.route('/create_group', methods=['POST'])
def create_group():
    if 'username' not in session:
        return redirect(url_for('login'))

    group_name = request.form['group_name']
    if group_name and group_name not in chat_history['group_chats']:
        chat_history['group_chats'][group_name] = []
        save_chat_history()

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)