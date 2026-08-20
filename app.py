import json

import streamlit as st

from extractor import extract_entities
from matcher import extract_candidate_profile, match_candidate_to_jd, suggest_job_roles
from resume_parser import UnsupportedFileType, parse_resume_bytes

st.set_page_config(page_title="AI Recruiter",
                   page_icon="🧑\u200d💼", layout="wide")

st.title("🧑\u200d💼 AI Recruiter")
st.caption(
    "An NLP-powered recruitment assistant that extracts skills from "
    "conversational text and resumes, suggests job roles, and matches "
    "candidates to job descriptions -- no LLM API required."
)

tab1, tab2, tab3 = st.tabs(
    ["🔎 Extractor (Part 1)", "🎯 Resume → Job Roles (Part 2)",
     "📄 Resume vs JD Match (Part 2)"]
)

# ---------------------------------------------------------------------------
# Part 1 - Extraction
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("Extract Skills, Technologies & Languages")
    st.write(
        "Paste conversational text describing experience (not a structured "
        "resume) and see the extracted entities as JSON."
    )

    default_example = "I worked in the AI/ML Department and worked with CNN Models using Python"
    user_text = st.text_area("Conversational input",
                             value=default_example, height=120)

    if st.button("Extract", key="extract_btn"):
        result = extract_entities(user_text)
        st.json(result)

        col1, col2, col3 = st.columns(3)
        col1.metric("Skills found", len(result["skill"]))
        col2.metric("Technologies found", len(result["technology"]))
        col3.metric("Languages found", len(result["language"]))

# ---------------------------------------------------------------------------
# Part 2a - Resume -> Job role suggestions
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("Upload a Resume to Get Job Role Suggestions")
    uploaded = st.file_uploader(
        "Resume file (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"], key="resume_roles"
    )
    top_k = st.slider("How many roles to suggest?",
                      min_value=1, max_value=10, value=5)

    if uploaded is not None:
        try:
            resume_text = parse_resume_bytes(
                uploaded.getvalue(), uploaded.name)
        except UnsupportedFileType as e:
            st.error(str(e))
            resume_text = None

        if resume_text:
            with st.expander("Show extracted resume text"):
                st.text(resume_text[:5000])

            profile = extract_candidate_profile(resume_text)
            st.markdown("**Extracted candidate profile**")
            st.json(profile)

            roles = suggest_job_roles(profile, top_k=top_k)
            st.markdown("**Suggested job roles**")
            for r in roles:
                with st.container(border=True):
                    st.markdown(f"### {r['role']} — {r['match_score']}% match")
                    st.progress(min(r["match_score"] / 100, 1.0))
                    st.caption(
                        f"Must-have coverage: {r['must_have_score']}% · "
                        f"Nice-to-have coverage: {r['nice_to_have_score']}%"
                    )
                    c1, c2 = st.columns(2)
                    c1.markdown("✅ **Matched must-have**")
                    c1.write(", ".join(r["matched_must_have"]) or "—")
                    c2.markdown("❌ **Missing must-have**")
                    c2.write(", ".join(r["missing_must_have"]) or "—")
                    c3, c4 = st.columns(2)
                    c3.markdown("➕ **Matched nice-to-have**")
                    c3.write(", ".join(r["matched_nice_to_have"]) or "—")
                    c4.markdown("○ **Missing nice-to-have**")
                    c4.write(", ".join(r["missing_nice_to_have"]) or "—")

# ---------------------------------------------------------------------------
# Part 2b - Resume vs Job Description matching
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Match a Resume Against a Job Description")
    uploaded_jd_resume = st.file_uploader(
        "Resume file (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"], key="resume_jd"
    )
    jd_text = st.text_area("Paste the job description here", height=200)

    if st.button("Run Match", key="match_btn"):
        if uploaded_jd_resume is None or not jd_text.strip():
            st.warning("Please upload a resume and paste a job description.")
        else:
            try:
                resume_text = parse_resume_bytes(
                    uploaded_jd_resume.getvalue(), uploaded_jd_resume.name
                )
            except UnsupportedFileType as e:
                st.error(str(e))
                resume_text = None

            if resume_text:
                result = match_candidate_to_jd(resume_text, jd_text)

                st.metric("Overall match score",
                          f"{result['overall_match_score']}%")
                c1, c2 = st.columns(2)
                c1.metric("Skill overlap score",
                          f"{result['skill_overlap_score']}%")
                c2.metric("Text similarity score",
                          f"{result['text_similarity_score']}%")

                c1, c2 = st.columns(2)
                c1.markdown("✅ **Matched requirements**")
                c1.write(", ".join(result["matched_requirements"]) or "—")
                c2.markdown("⚠️ **Missing requirements**")
                c2.write(", ".join(result["missing_requirements"]) or "—")

                with st.expander("Full match breakdown (JSON)"):
                    st.json(result)
