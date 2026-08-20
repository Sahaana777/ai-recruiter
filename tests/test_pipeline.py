"""
Simple smoke tests for the extraction and matching pipeline.
Run with:  python -m pytest tests/  (or just: python tests/test_pipeline.py)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from extractor import extract_entities
from matcher import extract_candidate_profile, match_candidate_to_jd, suggest_job_roles
from resume_parser import parse_resume

ROOT = Path(__file__).resolve().parent.parent


def test_spec_example():
    text = "I worked in the AI/ML Department and worked with CNN Models using Python"
    result = extract_entities(text)
    assert result["skill"] == ["AI/ML"]
    assert result["technology"] == ["CNN"]
    assert result["language"] == ["Python"]


def test_multi_entity_sentence():
    text = (
        "I have experience in Natural Language Processing and Computer "
        "Vision, using PyTorch, TensorFlow and OpenCV, mostly in Python "
        "and a bit of Java."
    )
    result = extract_entities(text)
    assert "Natural Language Processing" in result["skill"]
    assert "Computer Vision" in result["skill"]
    assert "PyTorch" in result["technology"]
    assert "TensorFlow" in result["technology"]
    assert "OpenCV" in result["technology"]
    assert "Python" in result["language"]
    assert "Java" in result["language"]


def test_empty_input():
    assert extract_entities("") == {"skill": [], "technology": [], "language": []}


def test_resume_parsing_and_role_suggestion():
    resume_text = parse_resume(str(ROOT / "sample_data" / "sample_resume.txt"))
    profile = extract_candidate_profile(resume_text)
    assert "Python" in profile["language"]
    assert "TensorFlow" in profile["technology"]

    roles = suggest_job_roles(profile, top_k=3)
    assert len(roles) == 3
    assert roles[0]["match_score"] >= roles[1]["match_score"] >= roles[2]["match_score"]
    top_role_names = [r["role"] for r in roles]
    assert "Machine Learning Engineer" in top_role_names or "NLP Engineer" in top_role_names


def test_resume_jd_matching():
    resume_text = parse_resume(str(ROOT / "sample_data" / "sample_resume.txt"))
    jd_text = parse_resume(str(ROOT / "sample_data" / "sample_jd.txt"))
    result = match_candidate_to_jd(resume_text, jd_text)
    assert 0 <= result["overall_match_score"] <= 100
    assert "Python" in result["matched_requirements"]


if __name__ == "__main__":
    tests = [
        test_spec_example,
        test_multi_entity_sentence,
        test_empty_input,
        test_resume_parsing_and_role_suggestion,
        test_resume_jd_matching,
    ]
    for t in tests:
        t()
        print(f"PASSED: {t.__name__}")
    print("\nAll tests passed.")
