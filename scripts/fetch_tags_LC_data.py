import json
import os 

file_name = "questions.json"
tag_list = set()

if os.path.exists(file_name):
    print("File Found")
    with open(file_name, 'r') as f:
        questions = json.load(f)
    for question in questions:
        for tag in question['tags']:
            tag_list.add(tag)

    unique_tags = len(tag_list)
    tag_list = sorted(list(tag_list))
    print(f"Total tags found: {unique_tags}")
    print(tag_list)
    print("Successfully added unique tags to list")
else:
    print("File NOT found")