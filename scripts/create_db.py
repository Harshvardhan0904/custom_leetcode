import sqlite3

def create_db():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS question(
        question_no INTEGET PRIMARY KEY,
        title       STRING,
        slug        STRING,
        difficulty  STRING,
        paid        INTEGER,                     
        tags        STRING,
        description STRING,
        exampleCase STRING,
        sampleCase  STRING           
        )
""")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS code_templates(
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
    print(f"[SUCCESSFULL]: Created tables :\n1. question.db\n2. code_template.db\nInside questions.db")

create_db()