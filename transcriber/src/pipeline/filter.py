import re


class TransitionFilter:
    """Filter out common transition segments from text."""

    def __init__(self):
        # Regex patterns for transitions
        self.patterns = [
            # Intro segment (split into parts since they appear as separate chunks)
            r"(?:and\s*)?I'?m\s*Nick(?:,?\s*(?:a|the))?\s*developing\s*parent(?:\s*(?:we'?re|and))?",
            r"(?:[Mm]y\s*name\s*is\s*)?Billy(?:\s*a)?\s*developmental\s*p[ae]diatrician(?:\s*and\s*I(?:\s*really)?\s*enjoy)?",
            r"We'?re\s*going\s*to\s*use\s*scenes\s*from\s*iconic\s*movies\s*to\s*talk\s*about\s*how\s*we\s*best\s*support\s*our\s*kids\.?",
            r"This\s*is\s*Pop\s*Culture\s*Parenting\.?",
            # Beer breath quotes (with variations)
            r"(?:Hey!?,?\s*)?(?:[Dd]on'?t\s*)?(?:let\s*)?(?:your\s*)?(?:mother|mom)(?:'?s)?\s*(?:catch(?:es)?|smell(?:ing)?|see(?:ing)?)\s*(?:that\s*)?beer(?:\s*(?:in|on|and)\s*(?:your\s*)?breath)?(?:,?\s*she'?ll\s*take\s*it\s*out\s*on\s*me)?\.?",
            r"[Uu]nless\s*(?:your\s*)?(?:mother|mom)(?:'?s)?\s*(?:catch(?:es)?|smell(?:ing)?|see(?:ing)?)\s*(?:that\s*)?beer(?:\s*(?:in|on)\s*(?:your\s*)?breath)?(?:,?\s*she'?ll\s*take\s*it\s*out\s*on\s*me)?\.?",
            r"(?:Hey!?,?\s*)?(?:[Dd]on'?t\s*)?(?:let\s*)?(?:your\s*)?(?:mother|mom)(?:'?s)?\s*(?:catch(?:es)?|smell(?:ing)?|see(?:ing)?)\s*(?:that\s*)?beer(?:\s*(?:in|on|and)\s*(?:your\s*)?breath)?(?:,?\s*she'?ll\s*take\s*it\s*out\s*on\s*me)?\.?",
            r"(?:S|s)mell\s*(?:that\s*)?beer(?:\s*(?:in|on|and)\s*(?:your\s*)?breath)?(?:,?\s*(?:she'?ll\s*take\s*it\s*out\s*on\s*me)?)?\.?",
            # Funk master quotes
            r"I\s*don'?t\s*object\s*to\s*fun\.?\s*I\s*love\s*fun\.?\s*In\s*fact,?\s*I'?m\s*the\s*grand\s*funk\s*master\s*of\s*fun\.?",
            r"(?:speaking\s*of\s*)?the\s*grand\s*funk\s*master\s*of\s*fun",
            # Daddy quote (split into parts since they appear separately)
            r"Who\s*is\s*your\s*daddy\??",
            r"(?:And\s*)?[Ww]hat\s*does\s*(?:it|he)\s*do\??",
            # Don't want to see quotes (with variations)
            r"I\s*don'?t\s*(?:want\s*to|wanna?)\s*see\s*(?:your?\s*)?(?:friends?\s*)?(?:again\s*)?(?:for\s*the\s*rest\s*of\s*my\s*whole\s*life)?\.?",
            r"I\s*don'?t\s*(?:want\s*to|wanna?)\s*see\s*anybody\s*else\s*(?:either|like\s*you)?\.?",
            # Trust/judgment quotes
            r"(?:Trust\s*you\s*is|Just\s*use|[Ww]e\s*trust\s*you)\s*(?:to\s*use\s*)?your\s*best\s*judgement?\.?",
            # Single word leftovers
            r"^\s*you\s*$",
            # Name/role restatements
            r"(?:Yes\.\s*)?[Ss]o\s*(?:yeah,?\s*)?(?:so\s*)?my\s*name\s*is\s*Billy\.?\s*I'?m\s*a\s*developmental\s*pediatrician",
            # Podcast references
            r"[Pp]op\s*[Cc]ulture\s*[Pp]arenting",
        ]

        # Combine all patterns with OR operator
        self.combined_pattern = "|".join(f"({p})" for p in self.patterns)

    def filter(self, text: str) -> str:
        """Filter out transition segments from text."""
        # Replace matches with empty string
        filtered_text = re.sub(
            self.combined_pattern, "", text, flags=re.IGNORECASE | re.MULTILINE
        )

        # Clean up any resulting empty lines or extra spaces
        filtered_text = re.sub(r"\n\s*\n", "\n", filtered_text)
        filtered_text = re.sub(r"\s+", " ", filtered_text)

        return filtered_text.strip()
