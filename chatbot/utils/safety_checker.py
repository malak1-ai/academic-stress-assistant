# utils/safety_checker.py

CRISIS_KEYWORDS = {
    "en": [
        "want to disappear", "hurt myself", "end it all", "can't go on",
        "no reason to live", "better off dead", "kill myself", "suicide",
        "self harm", "self-harm", "don't want to be here anymore",
        "wish i was dead", "want to die"
    ],
    "fr": [
        "veux disparaître", "me faire du mal", "en finir", "je veux mourir",
        "plus envie de vivre", "me suicider", "suicide", "automutilation",
        "je veux en finir", "plus envie d'être là", "mieux vaut mourir",
        "je me fais du mal"
    ],
    "ar": [
        "أريد أن أختفي", "أؤذي نفسي", "لا أريد الاستمرار", "أريد أن أموت",
        "انتحار", "إيذاء النفس", "مافيش سبب نعيش", "بغيت نموت",
        "بغيت نختفي", "ما بغيتش نكمل", "نقتل روحي", "ما بقاش عندي سبب"
    ]
}

HIGH_STRESS_KEYWORDS = {
    "en": [
        "stressed", "overwhelmed", "anxious", "panic", "panicking",
        "can't breathe", "can't cope", "breaking down", "losing it",
        "hopeless", "worthless", "exhausted", "burnout", "can't sleep",
        "failing", "giving up", "no point", "completely alone", "scared",
        "terrified", "numb", "empty", "falling apart", "nobody cares",
        "no one cares", "i give up", "so tired", "can't take it anymore",
        "i'm done", "too much", "falling behind", "i'm a failure"
    ],
    "fr": [
        "stressé", "dépassé", "anxieux", "panique", "je craque",
        "je n'en peux plus", "épuisé", "sans espoir", "inutile",
        "tout s'effondre", "je dors plus", "j'abandonne", "j'ai peur",
        "seul", "vide", "je me sens nul", "personne s'en fout",
        "burnout", "je vais craquer", "je peux plus", "trop de pression",
        "je suis nul", "ça va pas", "je suis perdu", "je tiens plus",
        "à bout", "plus la force", "je suis à plat"
    ],
    "ar": [
        "مضغوط", "قلقان", "خايف", "ماقدرش", "تعبت", "ما كنش",
        "مافيش فايدة", "ما قادرش ننعس", "راسي دايرة", "غالطني كلشي",
        "وحيد", "مكسور", "ما قادرش نتنفس", "نبكي بزاف", "ضغط",
        "توتر", "إجهاد", "يأس", "وحدة", "مش قادر نتحمل",
        "خلاص تعبت", "ما عندي حتى واحد", "فاشل", "مش عارف كيف نكمل",
        "كلشي غالط", "ما بقاش نقدر", "راني محتاج مساعدة"
    ]
}

MODERATE_STRESS_KEYWORDS = {
    "en": [
        "stressed", "worried", "nervous", "pressure", "deadline",
        "exam", "assignment", "grades", "procrastinating", "distracted",
        "unfocused", "tired", "behind on", "hard time", "struggling",
        "not sleeping well", "overwhelmed with", "too much work",
        "can't focus", "anxious about", "tension", "frustrated"
    ],
    "fr": [
        "inquiet", "nerveux", "pression", "deadline", "examen",
        "devoir", "notes", "procrastination", "distrait", "fatigué",
        "du mal à", "difficultés", "je dors mal", "trop de travail",
        "je n'arrive pas à me concentrer", "tendu", "frustré",
        "en retard sur", "stressé par", "préoccupé"
    ],
    "ar": [
        "قلقان على", "متوتر", "ضغط", "امتحان", "واجبات",
        "نقط", "تسويف", "مشتت", "تعبان", "ما نقدرش نركز",
        "ما نعسش مزيان", "بزاف ديال الشغل", "صعيب عليا",
        "متأخر على", "مقلق", "محتار", "مضغوط من"
    ]
}

# CHECKER
def check_safety(text: str) -> dict:
    """
    Scans user message for stress/crisis signals.

    Returns:
        {
            "level": "crisis" | "high" | "moderate" | "low",
            "matched_keywords": [...],
            "lang_hint": "en" | "fr" | "ar" | None
        }
    """
    text_lower = text.lower().strip()
    matched = []
    lang_hint = None

    #Check crisis first (highest priority)
    for lang, keywords in CRISIS_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                matched.append(kw)
                lang_hint = lang

    if matched:
        return {"level": "crisis", "matched_keywords": matched, "lang_hint": lang_hint}

    #Check high stress
    for lang, keywords in HIGH_STRESS_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                matched.append(kw)
                lang_hint = lang

    if matched:
        return {"level": "high", "matched_keywords": matched, "lang_hint": lang_hint}

    #Check moderate stress
    for lang, keywords in MODERATE_STRESS_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                matched.append(kw)
                lang_hint = lang

    if matched:
        return {"level": "moderate", "matched_keywords": matched, "lang_hint": lang_hint}

    #No signals detected
    return {"level": "low", "matched_keywords": [], "lang_hint": None}