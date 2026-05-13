import json

FILE_NAME = "questions.json"
def get_question_no(question_no: str):
    
    with open(FILE_NAME,"r") as f:
        questions = json.load(f)
    for question in questions :
        if question['question_no']==question_no:
            return question
    else:
        print("Question NOT found")