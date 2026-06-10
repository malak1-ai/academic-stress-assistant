# data/resources.py

# ---------------------------------------------------------------------------
# Support resources and hotlines in AR / FR / EN
# Focused on Morocco-based students + international fallback
# ---------------------------------------------------------------------------

RESOURCES = {
    "ar": {
        "hotline": "SOS Psychiatrie — 0800 008 008 (مجاني، 24/7)",
        "online": "findahelpline.com — ابحث عن خط مساعدة في بلدك",
        "campus": "تحدث مع مستشار الطلاب في جامعتك",
        "self_help": [
            "تطبيق Headspace — تأمل موجّه بالعربية والإنجليزية",
            "تطبيق Woebot — دعم نفسي مبني على العلاج المعرفي السلوكي",
            "موقع 7cups.com — دردشة مجانية مع متطوعين مدربين"
        ],
        "reminder": "طلب المساعدة شجاعة، مش ضعف. 💙"
    },
    "fr": {
        "hotline": "SOS Psychiatrie Maroc — 0800 008 008 (gratuit, 24h/24)",
        "online": "findahelpline.com — trouve une ligne d'aide dans ton pays",
        "campus": "Parle à un conseiller ou psychologue dans ton université",
        "self_help": [
            "Application Headspace — méditation guidée en français",
            "Application Woebot — soutien basé sur la thérapie cognitive",
            "Site 7cups.com — chat gratuit avec des bénévoles formés"
        ],
        "reminder": "Demander de l'aide, c'est courageux. Tu n'es pas seul(e). 💙"
    },
    "en": {
        "hotline": "SOS Psychiatrie Morocco — 0800 008 008 (free, 24/7)",
        "online": "findahelpline.com — find a helpline in your country",
        "campus": "Talk to a counselor or psychologist at your university",
        "self_help": [
            "Headspace app — guided meditation and stress relief",
            "Woebot app — CBT-based emotional support chatbot",
            "7cups.com — free chat with trained volunteer listeners"
        ],
        "reminder": "Reaching out takes courage. You are not alone. 💙"
    }
}


def get_resources(lang: str = "en") -> dict:
    """
    Returns the full resources dict for a given language.
    Falls back to English if language not found.
    """
    return RESOURCES.get(lang, RESOURCES["en"])


def get_hotline(lang: str = "en") -> str:
    """Returns just the hotline string for a given language."""
    return RESOURCES.get(lang, RESOURCES["en"])["hotline"]


def get_reminder(lang: str = "en") -> str:
    """Returns the encouragement reminder for a given language."""
    return RESOURCES.get(lang, RESOURCES["en"])["reminder"]


def get_self_help(lang: str = "en") -> list:
    """Returns the list of self-help tools for a given language."""
    return RESOURCES.get(lang, RESOURCES["en"])["self_help"]


def format_resources_message(lang: str = "en") -> str:
    """
    Returns a fully formatted resources message ready to display
    in the chat — used in high stress or crisis responses.
    """
    r = get_resources(lang)

    if lang == "ar":
        return (
            f"🆘 **إذا كنت بحاجة لمساعدة متخصصة:**\n\n"
            f"📞 {r['hotline']}\n"
            f"🌐 {r['online']}\n"
            f"🏫 {r['campus']}\n\n"
            f"🛠️ **أدوات مساعدة ذاتية:**\n"
            + "\n".join(f"• {item}" for item in r["self_help"])
            + f"\n\n{r['reminder']}"
        )
    elif lang == "fr":
        return (
            f"🆘 **Si tu as besoin d'aide spécialisée :**\n\n"
            f"📞 {r['hotline']}\n"
            f"🌐 {r['online']}\n"
            f"🏫 {r['campus']}\n\n"
            f"🛠️ **Outils d'auto-soutien :**\n"
            + "\n".join(f"• {item}" for item in r["self_help"])
            + f"\n\n{r['reminder']}"
        )
    else:
        return (
            f"🆘 **If you need specialized help:**\n\n"
            f"📞 {r['hotline']}\n"
            f"🌐 {r['online']}\n"
            f"🏫 {r['campus']}\n\n"
            f"🛠️ **Self-help tools:**\n"
            + "\n".join(f"• {item}" for item in r["self_help"])
            + f"\n\n{r['reminder']}"
        )