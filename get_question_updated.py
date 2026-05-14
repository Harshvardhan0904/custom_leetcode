import tabulate
import pandas as pd
import sqlite3

def map_question(tag_list: list):
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT question_no, title, slug, difficulty, paid, tags
        FROM question
        WHERE paid = 0
    """)
    rows = cursor.fetchall()
    conn.close()
    
    tags_set = set(tag_list)
    question_list = []
    
    for row in rows:
        question_tags = row[5].split(",")
        if any(tag in tags_set for tag in question_tags):
            question_list.append({
                "question_no": row[0],
                "title":       row[1],
                "slug":        row[2],
                "difficulty":  row[3],
                "paid_only":   bool(row[4]),
                "tags":        question_tags
            })
    
    return question_list

def format_tags(tags: list, max_tags: int = 3) -> str:
    if len(tags) <= max_tags:
        return ", ".join(tags)
    visible = ", ".join(tags[:max_tags])
    return f"{visible} +{len(tags) - max_tags} more"

def format_title(title: str, max_len: int = 30) -> str:
    return title if len(title) <= max_len else title[:max_len - 3] + "..."

def create_table(question_list: list):
    table_data = []
    for question in question_list:
        tags = question.get("tags", [])
        table_data.append({
            "Q_no":       question.get("question_no", "N/A"),
            "Title":      format_title(question.get("title", "N/A")),
            "Difficulty": question.get("difficulty", "N/A"),
            "Tags":       format_tags(tags, max_tags=3),
        })
    df = pd.DataFrame(table_data)
    df.index = df['Q_no']
    df.drop(columns="Q_no",inplace=True)
    print(tabulate.tabulate(df, headers="keys", tablefmt="rounded_grid"))

# test
questions = map_question(["Tree", "Array"])
create_table(questions)