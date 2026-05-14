import os
from config.config import PROBLEM_FOLDER_NAME, BASE_PROBLEM_LINK

os.makedirs(PROBLEM_FOLDER_NAME, exist_ok=True)


def create_file(file_name, mapped_lang, difficulty, user_question, code, cmt, desc):
    print("[CREATING TEMPLATE FOR THE QUESTION]")

    full_file_name  = f"{file_name}{mapped_lang}"
    file_saving_loc = os.path.join(PROBLEM_FOLDER_NAME, full_file_name)

    template = (
        f"{cmt} Question No : {user_question}\n"
        f"{cmt} Question    : {file_name}\n"
        f"{cmt} Difficulty  : {difficulty}\n"
        f"{cmt} Link        : {BASE_PROBLEM_LINK}{file_name}\n"
        f"{cmt} {'─' * 40}\n"
        f"{cmt} Description :\n"
        f"{desc}\n"
        f"{cmt} {'─' * 40}\n"
        f"{code}"
    )

    with open(file_saving_loc, "w", encoding="utf-8") as f:
        f.write(template)

    print(f"[DONE] Saved to: {file_saving_loc}")