import json

with open("questions.json") as f:
    questions = json.load(f)

with open("checkpoint.json") as f:
    checkpoint = json.load(f)

print(f"Questions saved : {len(questions)}")
print(f"Skip position   : {checkpoint['skip']}")
print(f"Fetched count   : {checkpoint['fetched']}")