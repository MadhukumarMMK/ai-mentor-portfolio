# ai-mentor-portfolio - Madhukumar



Criterion	Score (0-2)	What You Check in the Prompt
Clarity	0-2	Prompt asks for ONE clear goal like roadmap, logic-building, or consistency plan. Avoids confusing “do everything” instructions.
Beginner Context	0-2	Clearly mentions beginner students, B.Tech CSE audience, starting from zero, placement preparation, or learning struggles.
Specificity	0-2	Includes concrete requirements like daily schedule, coding exercises, logic-building methods, practice routines, consistency strategy, or 30-day roadmap.
Output Structure	0-2	Specifies output format clearly — JSON, step-by-step plan, weekly roadmap, tables, bullet points, or structured sections.
Practical Verification	0-2	Includes follow-up checks like beginner coding challenges, revision tasks, practice questions, progress tracking, or consistency measurement.



Day 2 Lab 2B — Errors handled
Markdown fence wrapping (\``json ... ````) The retry prompt asks Gemini to output raw JSON without fences. Triggers on ~5-10% of calls.

Hallucinated phone number when source has none Optional[str] = None in Pydantic — model returns null, schema validates.

Empty / whitespace-only input Pydantic raises ValidationError with "Field required". Caller catches.


Day 6 Lab 6A — Errors handled
Markdown fence wrapping (\``json ... ````) The retry prompt asks Gemini to output raw JSON without fences. Triggers on ~5-10% of calls.

Hallucinated phone number when source has none Optional[str] = None in Pydantic — model returns null, schema validates.

Empty / whitespace-only input Pydantic raises ValidationError with "Field required". Caller catches.

Hallucination on garbage input: Gemini sometimes invents a plausible résumé from non-résumé text. Defence: validate input before sending (e.g., minimum length, presence of email-like pattern).

Common bugs + recovery
Markdown ```json fences in output despite mime type → retry handles. If still failing, set temperature=0 in config.
Pydantic ValidationError: name Field required on a real résumé → add explicit hint to prompt: "The first line is the candidate's name."
429 Resource exhausted mid-batch → wait 60s + retry, OR switch to backup key. The afternoon Sprint 1 wires Groq fallback to handle this automatically.
Hallucinated résumé from garbage → flag in the room. This is the foundation of the Day 8 red-team: input sanity checks before LLM calls.

# Day 7 Lab 7A — ChromaDB Hello-World

- Embedded 10 syllabus paragraphs using MiniLM-L6-v2
- Stored embeddings in ChromaDB
- Performed semantic search
- Visualized embeddings using PCA
- Observed semantic clustering

Reflection:
Semantic search returns nearest meaning, not exact truth.
RAG systems need citation validation for correctness.

Day 9 Sprint 4 — Career Agent
Tools
jd_fetcher
skills_gap
answer_scorer
Learning
Agents select tools based on docstrings
Failure recovery is critical
ReAct traces help debugging
Tool contracts reduce hallucination
