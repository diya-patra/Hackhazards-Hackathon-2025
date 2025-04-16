from flask import Flask, render_template, request, jsonify
import json
from groq_api import ask_groq

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
