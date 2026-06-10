# main.py
from flask import Flask, request, jsonify, render_template, session
import uuid

from chatbot import get_response
from memory.session_manager import create_session, get_history, add_to_history
from prompts.language_templates import get_welcome_message
from config import FLASK_SECRET_KEY

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY


@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
        create_session(session["session_id"])
    return render_template("index.html")


@app.route("/welcome", methods=["GET"])
def welcome():
    """Returns Serene's hardcoded welcome message on page load."""
    welcome_msg = get_welcome_message()
    return jsonify({"message": welcome_msg})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "No message provided."}), 400

    user_message = data["message"].strip()
    session_id = session.get("session_id")

    if not session_id:
        session["session_id"] = str(uuid.uuid4())
        create_session(session["session_id"])
        session_id = session["session_id"]

    history = get_history(session_id)
    reply = get_response(user_message, history)

    add_to_history(session_id, role="user", content=user_message)
    add_to_history(session_id, role="assistant", content=reply)

    return jsonify({"reply": reply})  # ← this line is critical


@app.route("/reset", methods=["POST"])
def reset():
    """Wipes the session and starts a fresh conversation."""
    new_id = str(uuid.uuid4())
    session["session_id"] = new_id
    create_session(new_id)
    return jsonify({"status": "Session reset.", "session_id": new_id})


if __name__ == "__main__":
    app.run(debug=True)