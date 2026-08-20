import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from extractor import extract_entities

DATA_DIR = Path(__file__).resolve().parent / "data"

SKILL_WEIGHT = 0.7
TEXT_WEIGHT = 0.3

MUST_HAVE_WEIGHT = 0.75
NICE_TO_HAVE_WEIGHT = 0.25


def load_job_roles(data_dir: Path = DATA_DIR) -> dict:
    with open(data_dir / "job_roles.json", "r", encoding="utf-8") as f:
        return json.load(f)


JOB_ROLES = load_job_roles()


def _flatten_profile(entities: dict) -> set:
    combined = set()
    for cat in ("skill", "technology", "language"):
        combined.update(entities.get(cat, []))
    return combined


def extract_candidate_profile(resume_text: str) -> dict:
    return extract_entities(resume_text)


def suggest_job_roles(candidate_profile: dict, top_k: int = 5) -> list:

    candidate_set = _flatten_profile(candidate_profile)
    results = []

    for role, requirements in JOB_ROLES.items():
        must_have = set(requirements.get("must_have", []))
        nice_to_have = set(requirements.get("nice_to_have", []))
        if not must_have and not nice_to_have:
            continue

        matched_must = candidate_set & must_have
        matched_nice = candidate_set & nice_to_have

        must_score = (len(matched_must) / len(must_have)) if must_have else 1.0
        nice_score = (len(matched_nice) / len(nice_to_have)
                      ) if nice_to_have else 0.0

        weighted_score = (
            MUST_HAVE_WEIGHT * must_score + NICE_TO_HAVE_WEIGHT * nice_score
        )

        results.append(
            {
                "role": role,
                "match_score": round(weighted_score * 100, 1),
                "must_have_score": round(must_score * 100, 1),
                "nice_to_have_score": round(nice_score * 100, 1),
                "matched_skills": sorted(matched_must | matched_nice),
                "matched_must_have": sorted(matched_must),
                "missing_must_have": sorted(must_have - candidate_set),
                "matched_nice_to_have": sorted(matched_nice),
                "missing_nice_to_have": sorted(nice_to_have - candidate_set),
            }
        )

    results.sort(key=lambda r: r["match_score"], reverse=True)
    return results[:top_k]


def _text_similarity(text_a: str, text_b: str) -> float:
    if not text_a.strip() or not text_b.strip():
        return 0.0
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf = vectorizer.fit_transform([text_a, text_b])
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return float(sim)
    except ValueError:
        # e.g. both documents reduced to an empty vocabulary
        return 0.0


def match_candidate_to_jd(resume_text: str, jd_text: str) -> dict:
    candidate_entities = extract_entities(resume_text)
    jd_entities = extract_entities(jd_text)

    candidate_set = _flatten_profile(candidate_entities)
    jd_set = _flatten_profile(jd_entities)

    if jd_set:
        overlap = candidate_set & jd_set
        skill_score = len(overlap) / len(jd_set)
    else:
        overlap = set()
        skill_score = 0.0

    text_score = _text_similarity(resume_text, jd_text)
    final_score = SKILL_WEIGHT * skill_score + TEXT_WEIGHT * text_score

    return {
        "overall_match_score": round(final_score * 100, 1),
        "skill_overlap_score": round(skill_score * 100, 1),
        "text_similarity_score": round(text_score * 100, 1),
        "matched_requirements": sorted(overlap),
        "missing_requirements": sorted(jd_set - candidate_set),
        "candidate_profile": candidate_entities,
        "jd_requirements": jd_entities,
    }


if __name__ == "__main__":
    resume = (
        "Experienced software engineer skilled in Python and Java. "
        "Built machine learning models using TensorFlow and Scikit-learn, "
        "worked extensively with Pandas and NumPy for data analysis, "
        "and deployed services with Docker and AWS."
    )
    profile = extract_candidate_profile(resume)
    print("Candidate profile:", json.dumps(profile, indent=2))
    print("\nSuggested roles:")
    for r in suggest_job_roles(profile, top_k=3):
        print(f"  {r['role']}: {r['match_score']}% "
              f"(matched: {r['matched_skills']})")

    jd = (
        "Looking for a Machine Learning Engineer with strong Python skills, "
        "experience in TensorFlow, PyTorch, and deep learning, plus AWS "
        "deployment experience."
    )
    print("\nJD match:")
    print(json.dumps(match_candidate_to_jd(resume, jd), indent=2))
