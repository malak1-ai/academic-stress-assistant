# memory/session_manager.py
from config import MAX_HISTORY_LENGTH

# In-memory store: { session_id: [{"role": ..., "content": ...}, ...] }
_sessions = {}


def create_session(session_id: str) -> None:
    """Initializes a fresh empty conversation for a session."""
    _sessions[session_id] = []


def get_history(session_id: str) -> list:
    """Returns the full conversation history for a session."""
    return _sessions.get(session_id, [])


def add_to_history(session_id: str, role: str, content: str) -> None:
    """
    Appends a single turn to the session history.
    Trims oldest messages if history exceeds MAX_HISTORY_LENGTH,
    always keeping the first exchange for context continuity.
    """
    if session_id not in _sessions:
        create_session(session_id)

    _sessions[session_id].append({
        "role": role,
        "content": content
    })

    # Trim if too long — keep it within token-safe limits
    _trim_history(session_id)


def clear_session(session_id: str) -> None:
    """Wipes a session's history entirely (used on reset)."""
    _sessions[session_id] = []


def delete_session(session_id: str) -> None:
    """Removes a session from memory completely."""
    _sessions.pop(session_id, None)


def get_session_length(session_id: str) -> int:
    """Returns how many messages are stored in the session."""
    return len(_sessions.get(session_id, []))


def _trim_history(session_id: str) -> None:
    """
    Keeps history within MAX_HISTORY_LENGTH.
    Removes oldest pairs (user + assistant) from the middle,
    always preserving the first 2 messages (opening exchange)
    and the most recent messages.
    """
    history = _sessions[session_id]

    if len(history) <= MAX_HISTORY_LENGTH:
        return

    # Keep first 2 messages + most recent (MAX_HISTORY_LENGTH - 2)
    first_exchange = history[:2]
    recent = history[-(MAX_HISTORY_LENGTH - 2):]
    _sessions[session_id] = first_exchange + recent