from bs4 import BeautifulSoup
def get_lang(snippets)-> str:
    print("Language found:\n")
    lang_list = []
    for snippet in snippets['code_snippets']:
        lang = snippet['lang']
        lang_list.append(lang)
        print(f"- {lang}")
    lang_choice = input("From the above languages selet the language you want to write code:\n")
    lang_choice = lang_choice.strip()
    if lang_choice:
        if lang_choice in lang_list:
            print("[FOUND]")
            return lang_choice.lower()
        else:
            print(f"[NOT FOUND]: {lang_choice} Check for spelling")
            return None
    else:
        print("Please select a language")
        return None
    
def clean_text(response_with_html_tags):
    
    html_content = response_with_html_tags

    # Convert HTML -> clean text
    soup = BeautifulSoup(html_content, "html.parser")

    clean_text = soup.get_text()

    # Convert each line into Python comment
    comment_text = "\n".join(
        f"# {line}"
        for line in clean_text.splitlines()
        if line.strip()
    )

    return comment_text