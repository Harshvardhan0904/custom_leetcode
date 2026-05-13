import requests
from config.config import GRAPHQL_LINK, REFERENCE_LINK

def get_info(question_title: str):

    url = GRAPHQL_LINK

    query = """
    query questionEditorData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {

            title
            
            difficulty
            content
            exampleTestcases
            sampleTestCase

            topicTags {
                name
                slug
            }

            codeSnippets {
                lang
                langSlug
                code
            }
        }
    }
    """

    variables = {
        "titleSlug": question_title
    }

    headers = {
        "Content-Type": "application/json",
        "Referer": REFERENCE_LINK
    }

    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    data = response.json()

    question_data = data["data"]["question"]
    final_dict = {
        "title": question_data["title"],
        "difficulty": question_data["difficulty"],
        "description": question_data["content"],
        "example_testcases": question_data["exampleTestcases"],
        "sample_testcase": question_data["sampleTestCase"],
        "code_snippets": question_data["codeSnippets"],
        "tags":question_data['topicTags']
    }
    return final_dict