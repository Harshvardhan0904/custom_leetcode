import requests
import json
import os
import time
<<<<<<< HEAD
from config.config import GRAPHQL_LINK
from dotenv import load_dotenv

load_dotenv()
url = GRAPHQL_LINK

LEETCODE_SESSION = os.getenv('LEETCODE_SESSION')
CSRF_TOKEN = os.getenv('CSRF_TOKEN')
=======

url = "https://leetcode.com/graphql"

LEETCODE_SESSION = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfYXV0aF91c2VyX2lkIjoiOTc5MzYxMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjUyNTZhMDIyNGI3NjRhNTg2OGMzODU3Yzg4Y2RlMGQ5MWU2YTMwNzAzZWRiZGVhOGQyMmFiZDQyNmEzMmI1OGEiLCJzZXNzaW9uX3V1aWQiOiI5OTAyOWE1NSIsImlkIjo5NzkzNjExLCJlbWFpbCI6ImhhcnNodmFyZGhhbnQ4OEBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImhhcnNodmFyZGhhbnQ4OCIsInVzZXJfc2x1ZyI6ImhhcnNodmFyZGhhbnQ4OCIsImF2YXRhciI6Imh0dHBzOi8vYXNzZXRzLmxlZXRjb2RlLmNvbS91c2Vycy9hdmF0YXJzL2F2YXRhcl8xNjg2NDExNDg4LnBuZyIsInJlZnJlc2hlZF9hdCI6MTc3ODY5ODgwOCwiaXAiOiIyNDAxOjQ5MDA6OTFjMjpiZmE0OjhlZTo2NzlmOmE1ZjI6MzZhNSIsImlkZW50aXR5IjoiNjZjYWNlMmJkZWMxNDQ4YmRlN2Q5MWU5ZGExOWE5ZWMiLCJkZXZpY2Vfd2l0aF9pcCI6WyI0Yjc5ZDUzNzJjZjZkOWI1Njg2MzE5Yzg1MzdlMTgwNiIsIjI0MDE6NDkwMDo5MWMyOmJmYTQ6OGVlOjY3OWY6YTVmMjozNmE1Il19.H5BZV1z8PTqzSXeUn-xT21Xsac8XNoWjy4AuV-dqxfs"
CSRF_TOKEN = "og6jEaZY4TV3B2iA4FShmigSZGvW6e7n"
>>>>>>> 883cbfc45eb14b4d97e6f60f4741215f303a1664

headers = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com/problems/",
    "User-Agent": "Mozilla/5.0",
    "x-csrftoken": CSRF_TOKEN,
    "Cookie": f"LEETCODE_SESSION={LEETCODE_SESSION}; csrftoken={CSRF_TOKEN}"
}

QUESTIONS_FILE = "questions.json"
CHECKPOINT_FILE = "checkpoint.json"  # tracks where we left off

query = """
query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(
    categorySlug: $categorySlug
    limit: $limit
    skip: $skip
    filters: $filters
  ) {
    total: totalNum
    questions: data {
        questionId
        title
        titleSlug
        difficulty
        isPaidOnly
        content
        exampleTestcases
        sampleTestCase
        topicTags { name slug }
        codeSnippets { lang langSlug code }
    }
  }
}
"""

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as f:
            return json.load(f)
    return {"skip": 0, "fetched": 0}

def save_checkpoint(skip, fetched):
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump({"skip": skip, "fetched": fetched}, f)

def load_existing_questions():
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, 'r') as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    return []

def fetch_all_questions():
    # resume from checkpoint
    checkpoint = load_checkpoint()
    skip = checkpoint["skip"]

    # load already fetched questions
    all_questions = load_existing_questions()
    print(f"Resuming from skip={skip}, already have {len(all_questions)} questions.")

    limit = 50  # smaller batch = less timeout risk

    while True:
        variables = {
            "categorySlug": "",
            "limit": limit,
            "skip": skip,
            "filters": {}
        }

        try:
            response = requests.post(
                url,
                json={"query": query, "variables": variables},
                headers=headers,
                timeout=15  # fail fast instead of hanging
            )

            if not response.ok or not response.text.strip():
                print(f"Bad response at skip={skip}: {response.status_code}")
                save_checkpoint(skip, len(all_questions))
                break

            data = response.json()
            questions = data["data"]["problemsetQuestionList"]["questions"]
            total     = data["data"]["problemsetQuestionList"]["total"]

            for q in questions:
                all_questions.append({
                    "question_no": q["questionId"],
                    "title":       q["title"],
                    "slug":        q["titleSlug"],
                    "difficulty":  q["difficulty"],
                    "paid_only":   q["isPaidOnly"],
                    "tags":        [tag["name"] for tag in q["topicTags"]],
                    "code":        q["codeSnippets"] or [],
                    "description": q["content"] or "",
                    "exampleCase": q["exampleTestcases"],
                    "sampleCase":  q["sampleTestCase"],
                })

            skip += limit
            save_checkpoint(skip, len(all_questions))

            # save to file after every batch — no data loss on crash
            with open(QUESTIONS_FILE, 'w') as f:
                json.dump(all_questions, f, indent=2)

            print(f"Fetched {len(all_questions)}/{total}")
            time.sleep(0.5)  # be gentle with the server

            if skip >= total:
                print("All questions fetched!")
                os.remove(CHECKPOINT_FILE)  # clean up checkpoint
                break

        except requests.exceptions.Timeout:
            print(f"Timeout at skip={skip}. Saving checkpoint and retrying...")
            save_checkpoint(skip, len(all_questions))
            time.sleep(3)  # wait before retrying
            continue       # retry same batch

        except Exception as e:
            print(f"Unexpected error at skip={skip}: {e}")
            save_checkpoint(skip, len(all_questions))
            break

    return all_questions


questions = fetch_all_questions()
print(f"\nTotal questions fetched: {len(questions)}")