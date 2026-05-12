from utils.get_question_info import get_info
from utils.map_lang import map_lang
from utils.display import get_lang ,clean_text
from utils.fetcher import get_code_template, get_description
from utils.file_handler import create_file

def get_problem(imp_params_dict:dict, user_question: int):

    if user_question:
        if imp_params_dict[user_question]:
            print("[PROBLEM FOUND]")
            paid = imp_params_dict[user_question]['paid']
            if paid:
                print("[QUESTION REQUIRES PREMIUM SUBSCRIPTION]")
            else:
                print(imp_params_dict[user_question])
                slug = imp_params_dict[user_question]["slug"]
                snippets = get_info(question_title=slug)
                lang_choice = get_lang(snippets=snippets)
                code = get_code_template(snippets=snippets,lang_choice=lang_choice)
                desc,tags = get_description(snippets=snippets)
                desc = clean_text(response_with_html_tags=desc)
                difficulty = imp_params_dict[user_question]['difficulty']
                mapped_lang,comment_map = map_lang(lang=lang_choice)
                create_file(slug=slug,mapped_lang=mapped_lang,difficulty=difficulty,user_question=user_question,cmt=comment_map,code=code,desc=desc)
                print(tags)