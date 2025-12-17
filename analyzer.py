# analyzer.py
import re
import math
from typing import Dict, List, Tuple

# small sample common passwords (in practice use a bigger list file)
COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty", "abc123", "letmein",
    "admin", "welcome", "iloveyou", "passw0rd"
}

# helper checks
_seq_patterns = [
    "abcdefghijklmnopqrstuvwxyz",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "0123456789"
]

def _has_sequence(pw: str, length: int = 4) -> bool:
    s = pw
    for pat in _seq_patterns:
        for i in range(len(pat) - length + 1):
            seg = pat[i:i+length]
            if seg in s or seg[::-1] in s:
                return True
    return False

def _repeated_chars(pw: str, limit: int = 4) -> bool:
    return bool(re.search(r"(.)\1{" + str(limit-1) + r",}", pw))

def _character_pool_size(pw: str) -> int:
    pool = 0
    if re.search(r"[a-z]", pw): pool += 26
    if re.search(r"[A-Z]", pw): pool += 26
    if re.search(r"\d", pw): pool += 10
    if re.search(r"[^\w\s]", pw): 
        # count all common punctuation; approximate with 32 printable punctuation
        pool += 32
    return pool if pool > 0 else 1

def entropy(pw: str) -> float:
    """Estimate entropy in bits."""
    pool = _character_pool_size(pw)
    return len(pw) * math.log2(pool)

def analyze(password: str, common_passwords: set = COMMON_PASSWORDS) -> Dict:
    pw = password or ""
    e = entropy(pw)
    pool = _character_pool_size(pw)
    suggestions: List[str] = []
    score = 0.0

    # base score: normalize entropy
    # We'll map entropy of 0..80 bits to 0..100 (80 bits -> excellent)
    score = (e / 80.0) * 100.0
    score = max(0.0, min(100.0, score))

    # direct checks and penalties/bonuses
    if pw.lower() in common_passwords:
        score = 5.0
        suggestions.append("Password is a commonly used password — choose something unique.")
        category = "Very Weak"
        return {
            "password": pw,
            "entropy_bits": round(e, 2),
            "score": int(round(score)),
            "category": category,
            "suggestions": suggestions
        }

    if len(pw) < 8:
        suggestions.append("Use at least 8 characters.")
        score -= 15

    # variety bonus
    classes = sum(bool(re.search(p, pw)) for p in [r"[a-z]", r"[A-Z]", r"\d", r"[^\w\s]"])
    if classes <= 1:
        suggestions.append("Use a mix of uppercase, lowercase, digits and symbols.")
        score -= 10
    else:
        score += (classes - 1) * 3  # small bonus for variety

    if _repeated_chars(pw, limit=4):
        suggestions.append("Avoid long runs of the same character.")
        score -= 10

    if _has_sequence(pw, length=4):
        suggestions.append("Avoid common sequences like 'abcd' or '1234'.")
        score -= 10

    # final clamping
    score = max(0.0, min(100.0, score))

    # category
    if score < 25:
        category = "Very Weak"
    elif score < 50:
        category = "Weak"
    elif score < 70:
        category = "Fair"
    elif score < 90:
        category = "Strong"
    else:
        category = "Very Strong"

    if "Use a mix" not in suggestions and classes >= 3 and len(pw) >= 12:
        suggestions.append("Good: long password with character variety.")

    return {
        "password": pw,
        "entropy_bits": round(e, 2),
        "pool_size_est": pool,
        "score": int(round(score)),
        "category": category,
        "suggestions": suggestions
    }

# simple demo when run directly
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        pw = sys.argv[1]
    else:
        pw = input("Enter password to analyze: ")
    res = analyze(pw)
    from pprint import pprint
    pprint(res)
