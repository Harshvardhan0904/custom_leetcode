from rich import print
def show_language(question_info,question_no):
    
    code = question_info['code']
    
    print(f"Avaialbe languages for {question_no}:\n========")
    code_list = code.keys()
    for lang in code_list:
        print(lang)
    print("[bold yellow]Language name is case senitive so please enter same as mentioned in above list")