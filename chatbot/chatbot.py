# chatbot.py
import os
# TEMPORARY DEBUG — delete after fixing
from config import GROQ_API_KEY
print("=== KEY LOADED IN CHATBOT:", GROQ_API_KEY)

import requests
import json
from config import (
    GROQ_API_KEY,
    GROQ_BASE_URL,
    MODEL,
    TEMPERATURE,
    MAX_TOKENS,
    APP_NAME,
    APP_URL
)
from utils.safety_checker import check_safety
from utils.language_detector import detect_language
from data.resources import get_resources


# With this:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "system_prompt.txt")

with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

def get_response(user_message: str, history: list) -> str:

    # --- Step 1: Safety Check ---
    safety_result = check_safety(user_message)

    if safety_result["level"] == "crisis":
        lang = detect_language(user_message)
        resources = get_resources(lang)
        return _build_crisis_response(lang, resources)

    if safety_result["level"] == "high":
        extra_instruction = (
            "\n\n[INTERNAL NOTE — DO NOT MENTION THIS TO THE USER: "
            "The user shows high stress or distress signals. "
            "Be extra gentle, validate deeply before any advice, "
            "and at the end softly recommend professional help.]"
        )
    else:
        extra_instruction = ""

    # --- Step 2: Build messages ---
    messages = _build_messages(user_message, history, extra_instruction)
    def get_response(user_message: str, history: list) -> str:
        print("=== get_response called ===")  # ADD THIS
    
    try:                                   # ADD THIS
        # --- Step 1: Safety Check ---
        safety_result = check_safety(user_message)
        print("=== safety check passed:", safety_result)  # ADD THIS

        if safety_result["level"] == "crisis":
            lang = detect_language(user_message)
            resources = get_resources(lang)
            return _build_crisis_response(lang, resources)

        if safety_result["level"] == "high":
            extra_instruction = (
                "\n\n[INTERNAL NOTE — DO NOT MENTION THIS TO THE USER: "
                "The user shows high stress or distress signals. "
                "Be extra gentle, validate deeply before any advice, "
                "and at the end softly recommend professional help.]"
            )
        else:
            extra_instruction = ""

        messages = _build_messages(user_message, history, extra_instruction)
        print("=== messages built, calling Groq ===")  # ADD THIS
        return _call_groq(messages)

    except Exception as e:                 # ADD THIS
        print(f"=== FULL ERROR: {e}")      # ADD THIS
        import traceback                   # ADD THIS
        traceback.print_exc()              # ADD THIS
        return _fallback_message()         # ADD THIS

    # --- Step 3: Call Groq API ---
    return _call_groq(messages)


def _build_messages(user_message: str, history: list, extra_instruction: str = "") -> list:
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT + extra_instruction
        }
    ]

    for turn in history:
        messages.append({
            "role": turn["role"],
            "content": turn["content"]
        })

    messages.append({
        "role": "user",
        "content": user_message
    })

    return messages


def _call_groq(messages: list) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS
    }

    try:
        response = requests.post(
            GROQ_BASE_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        return _fallback_message()
    except requests.exceptions.RequestException as e:
        print(f"[Serene API Error]: {e}")
        print(f"[Response body]: {response.text}")
        return _fallback_message()
    except (KeyError, IndexError) as e:
        print(f"[Serene Parse Error]: {e}")
        return _fallback_message()


def _build_crisis_response(lang: str, resources: dict) -> str:
    if lang == "ar":
        return (
            "أنا هنا معك، وأنا سعيد/ة أنك تحدثت معي. 💙\n"
            "ما تشعر به الآن مهم جداً، وأنت لست وحدك.\n"
            f"أرجوك تحدث مع شخص متخصص يمكنه مساعدتك بشكل حقيقي:\n"
            f"📞 {resources['hotline']}\n"
            "أنت تستحق الدعم والمساعدة."
        )
    elif lang == "fr":
        return (
            "Je suis là avec toi, et je suis vraiment content(e) que tu m'en parles. 💙\n"
            "Ce que tu ressens est important, et tu n'es pas seul(e).\n"
            f"S'il te plaît, parle à quelqu'un qui peut vraiment t'aider:\n"
            f"📞 {resources['hotline']}\n"
            "Tu mérites du soutien."
        )
    else:
        return (
            "I'm right here with you, and I'm really glad you're talking to me. 💙\n"
            "What you're feeling matters, and you are not alone.\n"
            f"Please reach out to someone who can truly support you:\n"
            f"📞 {resources['hotline']}\n"
            "You deserve care and help."
        )


def _fallback_message() -> str:
    return (
        "I'm having a little trouble connecting right now. 🌿 "
        "Please give it a moment and try again — I'm here."
    )