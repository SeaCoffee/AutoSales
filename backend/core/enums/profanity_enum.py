import re


class ProfanityFilter:
    PATTERNS = (
        r'\bху[йиюе]\w*\b',
        r'\bп[ие]зд[ауы]\w*\b',
        r'\bбля[дть]\w*\b',
        r'\b[еи]ба[нт][аыуоий]*\w*\b',
        r'\bсра[нт][аыуоий]*\w*\b',
        r'\bговн\w*\b',
        r'\bгавн\w*\b',
        r'\bгімн\w*\b',
        r'\bїба[нт]\w*\b',
        r'\bйоба[нт]\w*\b',
    )

    COMPILED_PATTERNS = tuple(
        re.compile(pattern, flags=re.IGNORECASE)
        for pattern in PATTERNS
    )

    @classmethod
    def normalize(cls, text: str) -> str:
        return re.sub(r'\s+', ' ', str(text or '').lower()).strip()

    @classmethod
    def is_profane(cls, text: str) -> bool:
        normalized_text = cls.normalize(text)

        return any(
            pattern.search(normalized_text)
            for pattern in cls.COMPILED_PATTERNS
        )