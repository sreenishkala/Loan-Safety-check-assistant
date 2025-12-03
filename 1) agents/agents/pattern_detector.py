# agents/pattern_detector.py
import re
from typing import List

class PatternDetectorAgent:
    """
    Detects common predatory patterns using regex & heuristics.
    """
    def detect(self, text: str) -> List[str]:
        t = text.lower()
        flags = []

        # daily interest pattern (e.g., '9% per day','interest 9% per day')
        if re.search(r"\d+%.*per\s*day", t) or "per day" in t:
            flags.append("⚠ Detected daily interest pattern")

        # instant approval / instant loan
        if "instant" in t or "instant approval" in t:
            flags.append("⚠ Instant approval language (used by some scams)")

        # harassment / threat language
        if "contact your family" in t or "will contact your family" in t or "we will call" in t:
            flags.append("⚠ Harassment / pressure language detected")

        # large processing fee relative to loan amount (we'll check numerically in scorer)
        if re.search(r"processing fee", t) or re.search(r"processing charges", t):
            flags.append("⚠ Processing fee mentioned")

        # permission requests
        for perm in ["contacts", "gallery", "photos", "sms", "messages"]:
            if perm in t:
                flags.append(f"⚠ Permission requested: {perm}")

        return flags
