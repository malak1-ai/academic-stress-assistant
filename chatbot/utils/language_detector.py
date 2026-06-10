# utils/language_detector.py

# ---------------------------------------------------------------------------
# Language detection based on script + keyword fingerprints
# Supports: Arabic (ar), French (fr), English (en)
# Handles: Darija, Arabizi, mixed messages
# ---------------------------------------------------------------------------

# French fingerprint words — common in student conversation
FRENCH_MARKERS = [
    "je", "tu", "il", "elle", "nous", "vous", "ils", "elles",
    "est", "sont", "avoir", "être", "faire", "aller",
    "mais", "donc", "parce", "que", "qui", "quoi", "comment",
    "très", "bien", "mal", "plus", "tout", "rien", "avec",
    "pour", "dans", "sur", "pas", "non", "oui", "moi", "toi",
    "mon", "ma", "mes", "ton", "ta", "tes", "une", "les", "des",
    "stressé", "anxieux", "fatigué", "examen", "devoir", "école",
    "université", "notes", "prof", "cours"
]

# Arabizi fingerprints — Latin-script Moroccan Darija
ARABIZI_MARKERS = [
    "ana", "nta", "nti", "hna", "ntuma", "huma",
    "mashi", "wakha", "bghit", "mabghitsh", "kayn", "makaynsh",
    "zwina", "mezyan", "khouya", "khti", "safi", "walakin",
    "daba", "ghir", "bzaf", "chwiya", "fin", "kifash", "3lash",
    "7it", "m3a", "f", "b", "l", "wach", "ash", "aji",
    "mdarb", "mdrob", "t3ban", "magdarch", "khayf", "mrid"
]

# Arabic script range (Unicode blocks)
def _contains_arabic_script(text: str) -> bool:
    return any("\u0600" <= ch <= "\u06FF" for ch in text)


def _contains_latin_script(text: str) -> bool:
    return any("a" <= ch.lower() <= "z" for ch in text)


def _score_french(text: str) -> int:
    text_lower = text.lower()
    return sum(
        1 for marker in FRENCH_MARKERS
        if f" {marker} " in f" {text_lower} "
    )


def _score_arabizi(text: str) -> int:
    text_lower = text.lower()
    return sum(
        1 for marker in ARABIZI_MARKERS
        if f" {marker} " in f" {text_lower} "
    )


def detect_language(text: str, lang_hint: str = None) -> str:
    """
    Detects the language of the user's message.

    Priority order:
    1. Arabic script → "ar"
    2. Arabizi markers → "ar"
    3. French markers → "fr"
    4. lang_hint from safety_checker (bonus signal)
    5. Default → "en"

    Returns: "ar" | "fr" | "en"
    """
    if not text or not text.strip():
        return lang_hint or "en"

    # --- Arabic script (MSA or Darija written in Arabic) ---
    if _contains_arabic_script(text):
        return "ar"

    text_lower = text.lower().strip()

    # --- Arabizi detection ---
    arabizi_score = _score_arabizi(text_lower)
    french_score = _score_french(text_lower)

    if arabizi_score > 0 and arabizi_score >= french_score:
        return "ar"

    # --- French detection ---
    if french_score > 0:
        return "fr"

    # --- Use hint from safety checker if available ---
    if lang_hint in ("ar", "fr", "en"):
        return lang_hint

    # --- Default to English ---
    return "en"


def get_language_label(lang_code: str) -> str:
    """Returns a human-readable label for a language code."""
    labels = {
        "ar": "العربية / Darija",
        "fr": "Français",
        "en": "English"
    }
    return labels.get(lang_code, "English")