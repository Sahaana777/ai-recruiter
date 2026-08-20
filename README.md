# AI Recruiter — NLP + ChatBot Track

An NLP-powered recruitment assistant that extracts skills from conversational
text and resumes, suggests suitable job roles, and matches candidates to job
descriptions. Built for the MIC AIML Department Recruitment Challenge.

**Scope completed:** Part 1 (Extraction) + Part 2 (Matching).

## Project Overview

Recruiters spend a lot of time manually reading resumes, matching them to
open roles, and figuring out which candidates fit a job description. This
project automates the first pass of that process:

1. **Extraction** — turn a casual sentence like _"I worked with CNN models
   using Python"_ into structured JSON (`skill`, `technology`, `language`).
2. **Resume → Skills** — parse a real resume file and extract the same
   structured profile automatically.
3. **Job Role Suggestion** — given a candidate's profile, rank which job
   roles (ML Engineer, Data Scientist, Backend Developer, ...) they're the
   best fit for, with a transparent match percentage.
4. **Resume ↔ JD Matching** — given a resume and a job description, produce
   an explainable match score with matched/missing requirements.

## Problem Statement

Given the constraint of **no LLM API usage**, build a system that can reason
about skills, technologies, and programming languages purely with
traditional NLP techniques, and use that structured understanding to power
job-role suggestion and resume-to-JD matching — while keeping every score
explainable (not a black box).

## Installation Instructions

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd ai-recruiter

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Streamlit app
streamlit run app.py

# 5. (Optional) Run the test suite
python tests/test_pipeline.py
```

## Dataset Used

No external dataset is required for this project. Instead, the system uses
a **curated taxonomy** (`data/taxonomy.json`) of ~150 skills, technologies,
and programming-language aliases, and a **job-role profile bank**
(`data/job_roles.json`) mapping 14 common tech roles to their expected
skill sets. Sample resumes and job descriptions for testing/demo purposes
are provided in `sample_data/`.

This is a deliberate design choice for a closed-vocabulary extraction task:
gazetteer/taxonomy-based matching is a standard, explainable NLP approach
when the target entity set (skills, tech stacks, languages) is well-defined,
and it avoids the need for labeled training data or an LLM API key.

## Methodology

### Part 1 — Extraction (`extractor.py`)

1. **Tokenization** — a custom regex tokenizer that keeps symbol-bearing
   tech terms intact (`C++`, `Node.js`, `AI/ML`) instead of splitting on
   punctuation like a naive word tokenizer would.
2. **N-gram generation** — generates 1-to-4-word n-grams from the token
   stream, since many entities are multi-word phrases ("machine learning",
   "natural language processing").
3. **Greedy longest-match-first matching** — n-grams are checked against
   the taxonomy longest-first, so "machine learning" is matched as one
   phrase and doesn't ALSO get counted as the standalone word "learning".
   Matched token spans are tracked and excluded from further matching to
   prevent double-counting.
4. **Alias normalization** — the taxonomy maps many surface forms (`ml`,
   `machine learning`) to one canonical name (`Machine Learning`), so
   downstream matching logic only has to deal with canonical labels.

### Part 2 — Matching (`resume_parser.py`, `matcher.py`)

1. **Resume parsing** — `.pdf` (via `pdfplumber`), `.docx` (via
   `python-docx`), and `.txt` resumes are converted to plain text.
2. **Skill extraction from resumes** — the parsed resume text is run
   through the exact same Part 1 extraction pipeline, so resumes and
   conversational text share one consistent vocabulary.
3. **Job role suggestion** — for each of the 14 predefined roles, we
   compute `|candidate_skills ∩ role_required_skills| / |role_required_skills|`
   and rank roles by that percentage. This is intentionally simple and
   interpretable: a recruiter can see exactly which skills matched and
   which are missing for every suggestion.
4. **Resume ↔ JD matching** — combines two signals:
   - **Skill-overlap score (70% weight)** — same overlap logic as above,
     but against skills extracted from the specific job description
     instead of a fixed role profile.
   - **Text similarity score (30% weight)** — TF-IDF vectorization +
     cosine similarity between the full resume text and JD text, to catch
     relevant context the fixed taxonomy might miss.

   The weighted blend keeps the score mostly driven by _explainable_
   skill overlap, while still benefiting a little from broader textual
   relevance.

## Technologies Used

- **Python 3** — core language
- **scikit-learn** — `TfidfVectorizer` + `cosine_similarity` for text
  similarity scoring
- **pdfplumber** — PDF text extraction
- **python-docx** — DOCX text extraction
- **Streamlit** — interactive demo UI
- Standard library `re`, `json`, `pathlib` for tokenization and I/O

No LLM API key is used anywhere in this project, per the track requirements.

## Results

On the example from the challenge brief:

```
Input:  "I worked in the AI/ML Department and worked with CNN Models using Python"
Output: {"skill": ["AI/ML"], "technology": ["CNN"], "language": ["Python"]}
```

matches exactly (verified in `tests/test_pipeline.py::test_spec_example`).

On the bundled sample resume/JD (`sample_data/`), the pipeline:

- Extracts 9 distinct skills/technologies/languages from the resume.
- Ranks **Machine Learning Engineer** and **NLP Engineer** as the top
  suggested roles.
- Produces an overall resume↔JD match score in the 70–85% range, with a
  clear list of matched vs. missing requirements.

Run `python matcher.py` or the test suite for live output.

## Challenges Faced

- **Avoiding double/partial matches** — an early version of the extractor
  matched both "machine learning" and "learning" separately. Solved with
  greedy longest-n-gram-first matching plus span tracking to exclude
  already-matched tokens.
- **Symbol-heavy tokens** — a standard `\w+` tokenizer breaks `C++`,
  `Node.js`, and `AI/ML` into fragments. Required a custom regex
  tokenizer that preserves `+ # / . -` inside tokens.
- **Keeping match scores explainable** — it would have been easy to
  reduce matching to a single opaque similarity number. Instead every
  match result surfaces the actual matched/missing skill lists so the
  score can be justified, not just trusted.

## Future Improvements

- Expand the taxonomy and job-role bank (currently curated by hand;
  could be extended with a larger, community-maintained skills ontology).
- Add fuzzy string matching (e.g. edit distance) to catch typos or unseen
  spelling variants that aren't in the alias map.
- Weight required skills within a job role differently (e.g. "must-have"
  vs. "nice-to-have") instead of treating every required skill equally.
- Add a lightweight statistical NER model (e.g. spaCy) as a secondary
  extractor to catch skills/technologies outside the fixed taxonomy,
  falling back to the taxonomy for canonicalization.

## Screenshots

See the demo video for the Streamlit UI in action (extraction, resume
upload, job-role suggestions, and resume↔JD matching).

## Repository Structure

```
ai-recruiter/
├── app.py                  # Streamlit demo UI
├── extractor.py             # Part 1 - entity extraction engine
├── resume_parser.py         # Resume (PDF/DOCX/TXT) -> plain text
├── matcher.py                # Part 2 - role suggestion + JD matching
├── data/
│   ├── taxonomy.json         # Skills/technologies/languages + aliases
│   └── job_roles.json        # Job role -> required skill profiles
├── sample_data/
│   ├── sample_resume.txt
│   └── sample_jd.txt
├── tests/
│   └── test_pipeline.py      # Smoke tests for extraction + matching
├── requirements.txt
└── README.md
```
