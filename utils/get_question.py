import json
import tabulate
import pandas as pd

def map_question(tag_list: list):
    tags_set = set(tag_list)
    FILE_NAME = "questions.json"
    questions = []
    question_list = []

    try:
        with open(FILE_NAME, 'r') as f:
            content = f.read().strip()
            questions = json.loads(content) if content else []
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("File is empty or invalid JSON.")

    for question in questions:
        question_tags = question.get('tags', [])
        if isinstance(question_tags, str):
            question_tags = [question_tags]
        if any(tag in tags_set for tag in question_tags):
            question_list.append(question)

    return question_list


def format_tags(tags: list, max_tags: int = 3) -> str:
    if len(tags) <= max_tags:
        return ", ".join(tags)
    visible = ", ".join(tags[:max_tags])
    return f"{visible} +{len(tags) - max_tags} more"  # e.g. "Tree, Array, Hash Table +2 more"


def format_title(title: str, max_len: int = 30) -> str:
    return title if len(title) <= max_len else title[:max_len - 3] + "..."


# q_list = map_question(tag_list=['Tree'])

def create_table(question_list: list):
    table_data = []
    for question in question_list:
        tags = question.get('tags', [])
        table_data.append({
            "Q_no":       question.get('question_no', 'N/A'),
            "Title":      format_title(question.get('title', 'N/A')),
            "Difficulty": question.get('difficulty', 'N/A'),
            "Tags":       format_tags(tags, max_tags=3),
        })

    df = pd.DataFrame(table_data)
    df = df.reset_index(drop=True)
    print(tabulate.tabulate(df, headers='keys', tablefmt="rounded_grid"))