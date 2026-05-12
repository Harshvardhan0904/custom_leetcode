from utils.fetcher import fetch_problem
from utils.validator import get_problem

user_question = int(input("Enter question you want to solve:\n"))
imp_params_dict = fetch_problem()
get_problem(imp_params_dict=imp_params_dict,user_question=user_question)



