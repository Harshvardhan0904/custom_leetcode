import os
from config.config import PROBLEM_FOLDER_NAME, BASE_PROBLEM_LINK

os.makedirs(PROBLEM_FOLDER_NAME,exist_ok=True)
def create_file(slug,mapped_lang,difficulty,user_question,code,cmt,desc):
    print("[CREATING TEMPLATE FOR THE QUESTION]")
    file_name  = f"{slug}{mapped_lang}"
    file_saving_loc = os.path.join(PROBLEM_FOLDER_NAME,file_name)
    with open(file_saving_loc,"w") as f:
        f.write(f'''{cmt} Questiion: {user_question}\n{cmt} Qutestion name: {slug}\n{cmt} Difficulty: {difficulty}\n{cmt} Question link: {BASE_PROBLEM_LINK}{slug}\n{cmt} Description:\n{desc}\n\n{code}''')
        