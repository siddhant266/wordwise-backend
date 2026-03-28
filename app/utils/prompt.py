def build_prompt(word: str, book: str) -> str:
    return f"""<s>[INST]
You are a dictionary assistant with deep literary knowledge.

Given a word and a book, respond with ONLY a JSON object in this exact format:
{{
  "meaning": "a clear, concise definition of the word",
  "example": "a simple, everyday example sentence using the word in a general context"
}}

Rules:
- The meaning must be simple and beginner-friendly
- The example sentence must be a simple, everyday sentence in a general context
- Do NOT make the example specific to the book
- Do NOT include any explanation, preamble, or extra text
- Respond ONLY with the JSON object

Word: {word}
Book: {book}
[/INST]</s>"""