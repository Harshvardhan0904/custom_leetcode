import requests
import ast
from config.config import TAG_LIST
from rich.console import Console

console = Console()

def valid_tags(field: str) -> list[str]:
    """
    Generate relevant DSA tags for a given role/field using LLaMA.

    Args:
        field: The role or domain to generate tags for.

    Returns:
        A list of valid DSA tags, or empty list if domain is invalid.
    """
    prompt = f"""You are a LeetCode tag generator for coding interviews.

Task:
Return relevant LeetCode-style DSA tags for the role: "{field}"

Domain Validation (MOST IMPORTANT RULE):
- If the domain is not a real, recognized professional field or tech domain, return exactly: []
- Examples of INVALID domains: "banana", "xyz", "blahblah", "foo", "random gibberish"
- When in doubt, return: []

For valid domains:
- Think about what DSA topics are commonly tested for this role in interviews
- Include only fundamental DSA topics that interviewers actually test
- Use only tags from the allowed list below

Allowed tags:
{TAG_LIST}

Rules:
- Return ONLY a valid Python list, nothing else
- Use only tags from the allowed tags list above
- Do not explain anything
- Do not add extra text before or after the list
- Do not invent new tags
- For invalid domains return exactly: []

Example for "data science":
["Array", "Hash Table", "Math", "Sorting", "Matrix", "Dynamic Programming"]

Example for "banana":
[]
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

        if not raw:
            return []

        # Strip any extra text before/after the list
        start = raw.find("[")
        end = raw.rfind("]") + 1
        if start == -1 or end == 0:
            console.print("[red][Parse Error] No list found in model response.[/red]")
            return []

        raw_list = raw[start:end]

        # Safely parse the list
        tags = ast.literal_eval(raw_list)
        if not isinstance(tags, list):
            raise ValueError("Model response is not a list.")

        # Filter out any hallucinated tags not in TAG_LIST
        valid = [tag for tag in tags if tag in TAG_LIST]
        return valid

    except requests.exceptions.RequestException as e:
        console.print(f"[red][Request Error] Could not reach Ollama: {e}[/red]")
        return []
    except (ValueError, SyntaxError) as e:
        console.print(f"[red][Parse Error] Could not parse model response: {e}[/red]")
        console.print(f"[red]Raw response: {raw!r}[/red]")
        return []