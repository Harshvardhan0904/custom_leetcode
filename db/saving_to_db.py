import json
import sqlite3

def create_db():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS question (
            question_no  INTEGER PRIMARY KEY,
            title        TEXT,
            slug         TEXT,
            difficulty   TEXT,
            paid         INTEGER,
            tags         TEXT,
            description  TEXT,
            exampleCase TEXT,
            sampleCase  TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS code_templates (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            question_no  INTEGER,
            lang         TEXT,
            lang_slug    TEXT,
            code         TEXT,
            FOREIGN KEY (question_no) REFERENCES questions(question_no)
        )
    """)
    conn.commit()
    conn.close()

def save_all_questions(questions: list):
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    
    for i, q in enumerate(questions):
        cursor.execute("""
            INSERT OR IGNORE INTO question
            (question_no, title, slug, difficulty, paid, tags, description, exampleCase, sampleCase)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            int(q["question_no"]),
            q["title"],
            q["slug"],
            q["difficulty"],
            1 if q["paid_only"] else 0,
            ",".join(q["tags"]),
            q["description"],
            q.get("exampleCase", ""),
            q.get("sampleCase", "")
        ))
        
        if q.get("code"):
            for template in q["code"]:
                cursor.execute("""
                    INSERT OR IGNORE INTO code_templates
                    (question_no, lang, lang_slug, code)
                    VALUES (?, ?, ?, ?)
                """, (
                    int(q["question_no"]),
                    template["lang"],
                    template["langSlug"],
                    template["code"]
                ))
        else:
            print(f"No code for question {q['question_no']}")
        
        if i % 100 == 0:
            print(f"Saved {i}/{len(questions)}")
    
    conn.commit()
    conn.close()
    print("All questions saved to database")

# run
create_db()

with open("questions.json", "r") as f:
    questions = json.load(f)

save_all_questions(questions)