def show_language(question_info,question_no):
    code = question_info['code']
    print(f"Avaialbe languages for {question_no}:\n========")
    for lang in code:
        print(lang['lang'])