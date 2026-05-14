def show_language(question_info,question_no):
    print(question_info)
    code = question_info['code']
    print(code)
    print(f"Avaialbe languages for {question_no}:\n========")
    code_list = code.keys()
    for lang in code_list:
        print(lang)