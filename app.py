import streamlit as st
from google import genai
import json

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Résumé Scorer",
    layout="wide"
)

# ---------------------------------------------------
# App Header
# ---------------------------------------------------

st.title("Résumé vs JD Fit Scorer")
st.caption("Day 5 Lab 5A — Gemini + Continue.dev + Streamlit")

# ---------------------------------------------------
# Two Column Layout
# ---------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    resume = st.text_area(
        "Paste Résumé",
        height=400,
        placeholder="Paste the candidate résumé here..."
    )

with col2:
    jd = st.text_area(
        "Paste Job Description",
        height=400,
        placeholder="Paste the job description here..."
    )

# ---------------------------------------------------
# API Key Input
# ---------------------------------------------------

api_key = st.text_input(
    "Gemini API Key",
    type="password"
)

# Try loading from Streamlit secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

# ---------------------------------------------------
# Score Button Logic
# ---------------------------------------------------

if st.button("Score Résumé"):

    # Validation
    if not resume:
        st.warning("Please paste a résumé.")
        st.stop()

    if not jd:
        st.warning("Please paste a job description.")
        st.stop()

    if not api_key:
        st.warning("Please provide your Gemini API key.")
        st.stop()

    # Processing
    with st.spinner("Analyzing résumé against job description..."):

        try:

            # Gemini Client
            client = genai.Client(api_key=api_key)

            # Prompt
            prompt = f"""
You are an expert placement coach and technical recruiter.

Analyze the following résumé against the given job description.

Return ONLY valid JSON in this exact structure:

{{
  "score": 0,
  "rationale": "short explanation",
  "missing_skills": ["skill1", "skill2"],
  "suggestions": ["suggestion1", "suggestion2"],
  "technical_skills_match": 0,
  "soft_skills_match": 0,
  "experience_relevance": 0,
  "project_fit": 0,
  "learning_resources": [
    {{
      "skill": "Docker",
      "resource_type": "YouTube",
      "link": "https://youtube.com/example"
    }}
  ]
}}

Rules:
- score must be between 0 and 100
- all sub-scores must be between 0 and 100
- return only real missing skills
- suggestions must be practical
- learning_resources must contain free resources
- return ONLY JSON
- do not add markdown
- do not add explanations outside JSON

Résumé:
{resume}

Job Description:
{jd}
"""

            # Generate Gemini Response
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                }
            )

            # Parse JSON
            result = json.loads(response.text)

            # ---------------------------------------------------
            # Display Main Score
            # ---------------------------------------------------

            st.success("Analysis Completed")

            st.metric(
                label="Overall Fit Score",
                value=f"{result.get('score', 0)}/100"
            )

            # ---------------------------------------------------
            # Score Breakdown
            # ---------------------------------------------------

            st.subheader("Score Breakdown")

            breakdown = {
                "Technical Skills": result.get(
                    "technical_skills_match", 0
                ),
                "Soft Skills": result.get(
                    "soft_skills_match", 0
                ),
                "Experience": result.get(
                    "experience_relevance", 0
                ),
                "Project Fit": result.get(
                    "project_fit", 0
                )
            }

            st.bar_chart(breakdown)

            # ---------------------------------------------------
            # Rationale
            # ---------------------------------------------------

            st.subheader("Rationale")

            st.write(
                result.get("rationale", "No rationale provided.")
            )

            # ---------------------------------------------------
            # Missing Skills
            # ---------------------------------------------------

            st.subheader("Missing Skills")

            missing_skills = result.get(
                "missing_skills", []
            )

            if missing_skills:
                for skill in missing_skills:
                    st.write(f"• {skill}")
            else:
                st.write("No major missing skills detected.")

            # ---------------------------------------------------
            # Suggestions
            # ---------------------------------------------------

            st.subheader("Suggestions")

            suggestions = result.get(
                "suggestions", []
            )

            if suggestions:
                for suggestion in suggestions:
                    st.write(f"• {suggestion}")
            else:
                st.write("No suggestions available.")

            # ---------------------------------------------------
            # Learning Resources
            # ---------------------------------------------------

            st.subheader(
                "Top Missing Skills with Learning Resources"
            )

            learning_resources = result.get(
                "learning_resources", []
            )

            if learning_resources:

                for item in learning_resources:

                    skill = item.get("skill", "Unknown Skill")
                    resource_type = item.get(
                        "resource_type",
                        "Resource"
                    )
                    link = item.get("link", "")

                    st.markdown(
                        f"""
- **{skill}**
  - Type: {resource_type}
  - Link: {link}
"""
                    )

            else:
                st.write("No learning resources available.")

        # ---------------------------------------------------
        # JSON Error Handling
        # ---------------------------------------------------

        except json.JSONDecodeError:

            st.error(
                "Could not parse Gemini response as JSON."
            )

            st.write(response.text)

        # ---------------------------------------------------
        # General Error Handling
        # ---------------------------------------------------

        except Exception as e:

            st.error("An error occurred.")

            st.exception(e)