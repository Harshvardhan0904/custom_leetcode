import click
from utils.file_handler import create_file
from utils.llm_cache import get_tags_from_domain
from utils.get_question import map_question, create_table
from utils.get_all_info import get_question
from utils.get_available_languages import show_language
from utils.map_lang import map_lang
from utils.display import clean_text


def prompt(msg: str) -> str:
    
    while True:
        val = input(msg).strip()
        if val:
            return val
        print("Input cannot be empty. Please try again.\n")


def main():
   
    field = prompt("Tell about the field you are interested in:\n").lower()

    try:
        related_tags = get_tags_from_domain(domain=field)
    except Exception as e:
        print(f"Failed to fetch tags for '{field}': {e}")
        return
    print("Tags for the field requested:\n", related_tags)

    
    try:
        question_list = map_question(tag_list=related_tags)
        create_table(question_list=question_list)
    except Exception as e:
        print(f"Failed to fetch questions: {e}")
        return


    question_id = prompt("From the above listed questions, select a question number you want to solve:\n")

    try:
        question_info = get_question(question_no=question_id)
    except Exception as e:
        print(f"Could not fetch question '{question_id}': {e}")
        return

    show_language(question_info=question_info, question_no=question_id)
    language_input = prompt("From the above languages, choose one to solve the question:\n").strip()

    try:
        extension, comment_syntax = map_lang(lang=language_input)
    except Exception as e:
        print(f"Unsupported language '{language_input}': {e}")
        return


    raw_description = question_info['description']
    clean_desc = clean_text(response_with_html_tags=raw_description, comment_tag=comment_syntax)

    question_title = question_info['slug']
    difficulty = question_info['difficulty']

    lang = list(question_info['code'].keys())
    code_template = list(question_info['code'].values())
    code_str = question_info['code'].get(language_input, None)
    if code_str is None:
        print(f"No code template found for '{language_input}'. Please try a different language.")
        return

    try:
        create_file(
            file_name=question_title,
            mapped_lang=extension,
            difficulty=difficulty,
            user_question=question_id,
            code=code_str,
            cmt=comment_syntax,
            desc=clean_desc
        )
        print(f"\nFile created successfully for '{question_title}' in {language_input}!")
    except Exception as e:
        print(f"Failed to create file: {e}")


if __name__ == "__main__":
    main()