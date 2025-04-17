from flask import session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, jsonify
import json
from groq_api import ask_groq


app = Flask(__name__)

app.secret_key = "super_secret_key"  # Needed for session


# ---------------- Pages ----------------
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")

@app.route('/group')
def group_chat():
    return render_template("group_chat.html")

@app.route('/about')
def about():
    return render_template("about.html")

# ---------------- API: Chatbot ----------------
@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = ask_groq(user_message)
    return jsonify({"response": response})

# ---------------- API: Group Chat ----------------
@app.route('/api/group_chat', methods=['GET', 'POST'])
def handle_group_chat():
    with open('chat_data.json', 'r+') as file:
        data = json.load(file)
        if request.method == 'POST':
            new_message = request.json
            data.append(new_message)
            file.seek(0)
            json.dump(data, file, indent=2)
            return jsonify({"status": "Message added"})
        else:
            return jsonify(data)
        
import os

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        if not os.path.exists('users.json'):
            with open('users.json', 'w') as f:
                json.dump([], f)

        with open('users.json', 'r+') as f:
            users = json.load(f)
            if any(u['email'] == email for u in users):
                return "Email already registered."
            users.append({"username": username, "email": email, "password": password})
            f.seek(0)
            json.dump(users, f, indent=2)
        return redirect('/login')

    return render_template("signup.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with open('users.json', 'r') as f:
            users = json.load(f)

        user = next((u for u in users if u['email'] == email), None)
        if user and check_password_hash(user['password'], password):
            session['user'] = user['username']
            return redirect('/chatbot')
        else:
            return "Invalid login."

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

