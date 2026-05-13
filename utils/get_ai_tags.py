import requests
import ast
from config.config import TAG_LIST


def valid_tags(field: str) -> list[str]:
    """
    Generate relevant DSA tags for a given role/field using LLaMA.
    
    Args:
        field: The role or domain to generate tags for.
    
    Returns:
        A list of valid DSA tags.
    """
    prompt = f"""You are a LeetCode tag generator for coding interviews.

Task:
Return relevant LeetCode-style DSA tags for coding interviews targeting the role: "{field}"

Important:
- Think about what coding/DSA topics are commonly tested for this role
- Add what type of coding questions are genrally asked in that field in interview
- Include fundamental DSA topics that interviewers actually test

Allowed tags:
{TAG_LIST}

Rules:
- Return ONLY a valid Python list
- Use only tags from the allowed tags list
- Do not explain anything
- Do not add extra text
- Do not invent new tags

Example for "Data Science":
["Array", "Hash Table", "Math", "Sorting", "Matrix", "Dynamic Programming"]
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
            },
            timeout=30,
        )
        response.raise_for_status()

        raw = response.json().get("response", "").strip()

        # Safely parse the list from the model's response
        tags = ast.literal_eval(raw)

        if not isinstance(tags, list):
            raise ValueError("Model response is not a list.")

        # Filter out any hallucinated tags not in TAG_LIST
        valid = [tag for tag in tags if tag in TAG_LIST]
        return valid

    except requests.exceptions.RequestException as e:
        print(f"[Request Error] Could not reach Ollama: {e}")
        return []
    except (ValueError, SyntaxError) as e:
        print(f"[Parse Error] Could not parse model response: {e}")
        print(f"Raw response: {raw!r}")
        return []
