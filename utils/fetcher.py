import requests
from config.config import PROBLEM_LINK

def fetch_problem()-> dict:
    response = requests.get(PROBLEM_LINK)
    map_diff = {1: "Easy", 2: "Medium", 3: "Hard"}
    if response.status_code == 200:
        print("[CONNECTED]")
    else:
        print(f"[FAILED]: Status code: {response.status_code}")
    data = response.json()
    all_problem_list = data['stat_status_pairs']
    imp_params_dict = {}
    for problem in all_problem_list:
        question_no = problem['stat']['frontend_question_id']
        difficulty  = map_diff[problem['difficulty']['level']]
        paid        = problem['paid_only']
        title       = problem['stat']['question__title']
        slug        = problem['stat']['question__title_slug']

        imp_params_dict[question_no] = {
            "title":      title,
            "slug":       slug,
            "difficulty": difficulty,
            "paid":       paid
        }
    return imp_params_dict


def get_code_template(snippets,lang_choice):
    for snippet in snippets['code_snippets']:
        if snippet['lang'].lower() ==lang_choice:
            code_str = snippet['code']
            return code_str
    else:
        print("[CODE TEMPLATE NOT FOUND]")

def get_description(snippets):
    tag_list = []
    desc = snippets['description']
    for i in snippets['tags']:
        tag_list.append(i['slug'])
    return desc, tag_list