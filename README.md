# 🦆 LazyLeetCode

> AI-powered LeetCode practice CLI that maps your domain to relevant problems and opens them directly in VS Code.

---

## What It Does

Instead of manually browsing LeetCode, LazyLeetCode asks what domain you're targeting (backend, ML, frontend etc.), uses a local AI model to find the most relevant LeetCode tags for that domain, filters all free questions by those tags, and opens your chosen problem as a ready-to-solve file directly in VS Code.

```
You type your domain
        ↓
AI generates relevant LeetCode tags
        ↓
Free questions filtered by those tags
        ↓
You pick a question and language
        ↓
File opens in VS Code with problem + starter code
```

---

## Demo

```
$ python debugduck.py

🦆 LazyLeetCode — AI Powered LeetCode Practice

What domain are you interested in? → backend development

Generating tags with AI...
Tags found: ['Array', 'Hash Table', 'Sliding Window', 'Binary Search', 'Tree']

Fetching questions...
Found 63 relevant free questions

Pick difficulty:
1. Easy
2. Medium
3. Hard
4. All
→ 2

┌─────┬──────────────────────────────────┬────────────┬───────────────────────┐
│ No  │ Title                            │ Difficulty │ Tags                  │
├─────┼──────────────────────────────────┼────────────┼───────────────────────┤
│ 3   │ Longest Substring Without...     │ Medium     │ Hash Table, Sliding.. │
│ 49  │ Group Anagrams                   │ Medium     │ Hash Table, String    │
│ 347 │ Top K Frequent Elements          │ Medium     │ Array, Hash Table     │
└─────┴──────────────────────────────────┴────────────┴───────────────────────┘

Pick a question (number) → 2

Pick language:
1. Python
2. JavaScript
3. Java
4. C++
→ 1

Opening group_anagrams.py in VS Code...
Submit here: https://leetcode.com/problems/group-anagrams
```

---

## Prerequisites

Before running DebugDuck you need:

- Python 3.8+
- VS Code with the `code` command in PATH
- Ollama installed and running → [ollama.com](https://ollama.com)

### Setting Up Ollama

```bash
# 1. Download Ollama from https://ollama.com and install it

# 2. Pull the model (one time, ~2GB download)
ollama pull llama3.2

# 3. Make sure the Ollama app is running before using DebugDuck
```

---

## Installation

```bash
# 1. Clone the repo
git clone (https://github.com/Harshvardhan0904/custom_leetcode)
cd debugduck

# 2. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Fetch LeetCode questions (one time)
python fetch.py
```

---

## Usage

```bash
python LazyLeetCode.py
```

On first run the tool fetches all free LeetCode questions and caches them locally in `questions.json`. Every run after that is instant — no repeated API calls.

---

## How It Works

### 1. Domain to Tags via Local AI
Your domain input is sent to a local LLaMA 3.2 model running via Ollama. The model picks the most relevant tags from LeetCode's actual tag list — no hallucination possible since it chooses from a fixed known list.

### 2. Question Filtering
All questions are fetched once from LeetCode's GraphQL API and cached locally. They are filtered by:
- Matching AI-generated tags
- Free questions only (`paid_only = false`)
- Your chosen difficulty level

### 3. File Generation
The chosen question is written to a `.py` / `.js` / `.java` / `.cpp` file with:
- Question number and difficulty
- Problem description
- Direct LeetCode link for submission
- Language-specific starter code

### 4. VS Code Integration
The file opens automatically in VS Code. Solve it there, then use the link in the file to submit on LeetCode.

---

## Project Structure

```
debugduck/
├── debugduck.py        # main entry point and CLI flow
├── fetch.py            # LeetCode GraphQL fetching
├── llm.py              # Ollama integration
├── questions.json      # cached questions (auto generated)
├── requirements.txt    # dependencies
└── README.md
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Ollama + LLaMA 3.2 | Local AI for tag generation |
| LeetCode GraphQL API | Question fetching |
| Rich | CLI formatting and tables |
| SQLite | Progress tracking (v2) |
| VS Code CLI | Opening problem files |

---

## Roadmap

- [x] Domain to tag mapping via local AI
- [x] Free question filtering by tags and difficulty
- [x] Language-specific file generation
- [x] VS Code integration
- [ ] Progress tracking with SQLite
- [ ] Spaced repetition for question review
- [ ] Streak tracking
- [ ] AI-powered weak area detection
- [ ] Interview readiness score
- [ ] `pip install LazyLeetCode` support

---

## Why LazyLeetCode

Most developers know which LeetCode topics matter for their domain — but browsing, filtering, and setting up a problem every time adds friction. DebugDuck removes that friction entirely. One command, answer three questions, start solving.

The rubber duck is there to judge you silently.

---

## Contributing

Pull requests are welcome. For major changes please open an issue first.

---

## Author

Built by [Harsh Vardhan Tiwari]  
If this helped you land a job, star the repo. 🦆
