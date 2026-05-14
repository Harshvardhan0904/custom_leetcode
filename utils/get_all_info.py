import sqlite3
def get_question(question_no: int):
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT q.question_no, q.title, q.slug, q.difficulty, q.paid, q.tags, q.description, ct.code, ct.lang
        FROM question q
        JOIN code_templates ct ON q.question_no = ct.question_no
        WHERE q.question_no = ?
    """, (question_no,))
    
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print(f"Question {question_no} not found")
        return None
    
    # first row has all question data
    first = rows[0]
    
    # collect all language codes from all rows
    codes = {row[8]: row[7] for row in rows}   # {"python3": "...", "java": "..."}
    
    return {
        "question_no": first[0],
        "title":       first[1],
        "slug":        first[2],
        "difficulty":  first[3],
        "paid_only":   bool(first[4]),
        "tags":        first[5].split(","),
        "description": first[6],
        "code":       codes       # all languages available
    }

# access specific language