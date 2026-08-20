import difflib
import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

_CATEGORY_TO_OUTPUT_KEY = {
    "skills": "skill",
    "technologies": "technology",
    "languages": "language",
}

MAX_NGRAM = 4

# Fuzzy-matching (typo tolerance) settings.
FUZZY_MIN_TOKEN_LEN = 4      # don't fuzzy-match very short words (too noisy)
FUZZY_CUTOFF = 0.82          # similarity threshold (0-1), higher = stricter
FUZZY_MAX_LEN_DIFF = 2       # only compare tokens within N chars of candidate


def load_taxonomy(data_dir: Path = DATA_DIR) -> dict:
    with open(data_dir / "taxonomy.json", "r", encoding="utf-8") as f:
        return json.load(f)


TAXONOMY = load_taxonomy()


def _tokenize(text: str):
    """Tokenize while preserving symbols common in tech terms: + # / . -"""
    text = text.replace("\u2019", "'")
    tokens = re.findall(r"[A-Za-z0-9][A-Za-z0-9+#./\-]*", text)
    # strip a lone trailing '.' from a token (end-of-sentence artifact),
    # but keep things like "Node.js" intact
    cleaned = []
    for tok in tokens:
        if tok.endswith(".") and not re.search(r"\.[A-Za-z]", tok):
            tok = tok[:-1]
        if tok:
            cleaned.append(tok)
    return cleaned


def _generate_ngrams(tokens, n):
    return [
        (i, i + n, " ".join(tokens[i:i + n]))
        for i in range(len(tokens) - n + 1)
    ]


def _overlaps(span, matched_spans):
    start, end = span
    for s, e in matched_spans:
        if start < e and s < end:  # ranges intersect
            return True
    return False


_SINGLE_WORD_KEYS = {
    category: [k for k in alias_map if " " not in k]
    for category, alias_map in TAXONOMY.items()
}


def _fuzzy_match_token(token: str):

    if len(token) < FUZZY_MIN_TOKEN_LEN:
        return None

    token_lower = token.lower()
    best = None
    best_ratio = 0.0

    for category, keys in _SINGLE_WORD_KEYS.items():
        candidates = [
            k for k in keys
            if abs(len(k) - len(token_lower)) <= FUZZY_MAX_LEN_DIFF
        ]
        matches = difflib.get_close_matches(
            token_lower, candidates, n=1, cutoff=FUZZY_CUTOFF
        )
        if not matches:
            continue
        ratio = difflib.SequenceMatcher(None, token_lower, matches[0]).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best = (category, TAXONOMY[category][matches[0]], matches[0])

    return best


def extract_entities(text: str, fuzzy: bool = True) -> dict:

    if not text or not text.strip():
        return {"skill": [], "technology": [], "language": [], "corrections": []}

    tokens = _tokenize(text)
    found = {"skill": set(), "technology": set(), "language": set()}
    matched_spans = []
    corrections = []

    # Pass 1: exact matching, longest n-grams first so multi-word phrases
    # win over sub-words.
    for n in range(min(MAX_NGRAM, len(tokens)), 0, -1):
        for start, end, phrase in _generate_ngrams(tokens, n):
            span = (start, end)
            if _overlaps(span, matched_spans):
                continue
            key = phrase.lower()
            for category, alias_map in TAXONOMY.items():
                if key in alias_map:
                    output_key = _CATEGORY_TO_OUTPUT_KEY[category]
                    found[output_key].add(alias_map[key])
                    matched_spans.append(span)
                    break

    # Pass 2: fuzzy matching on leftover single tokens (typo tolerance).
    if fuzzy:
        for i, tok in enumerate(tokens):
            span = (i, i + 1)
            if _overlaps(span, matched_spans):
                continue  # already matched exactly, or part of a longer match
            result = _fuzzy_match_token(tok)
            if result:
                category, canonical, matched_alias = result
                output_key = _CATEGORY_TO_OUTPUT_KEY[category]
                found[output_key].add(canonical)
                matched_spans.append(span)
                corrections.append(
                    {"input": tok, "matched": canonical, "category": output_key}
                )

    return {
        "skill": sorted(found["skill"]),
        "technology": sorted(found["technology"]),
        "language": sorted(found["language"]),
        "corrections": corrections,
    }


if __name__ == "__main__":
    sample = "I worked in the AI/ML Department and worked with CNN Models using Python"
    print(json.dumps(extract_entities(sample), indent=2))
