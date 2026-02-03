EXTRACT_PROMPT = """
Extract ONLY the MCQ questions that already exist in this document.
DO NOT generate new questions.

For each question, extract:
- question
- options (A/B/C/D)
- correct answer (if present)
- explanation (if present)

Language: Bangla or English (keep original)

Return STRICT JSON array.
"""

GENERATE_PROMPT = """
Generate high-quality MCQ questions from this content.

Rules:
- Create meaningful MCQs
- 4 options (A/B/C/D)
- One correct answer
- Short explanation
- Language: Bangla or English (match content)

Return STRICT JSON array.
"""

CUSTOM_PROMPT_TEMPLATE = """
{user_prompt}

Rules:
- Use only the document content
- Language: Bangla or English
- Return STRICT JSON array
"""
