from bs4 import BeautifulSoup

def clean_text(response_with_html_tags,comment_tag:str):
    
    html_content = response_with_html_tags

    # Convert HTML -> clean text
    soup = BeautifulSoup(html_content, "html.parser")

    clean_text = soup.get_text()

    # Convert each line into Python comment
    comment_text = "\n".join(
        f"{comment_tag} {line}"
        for line in clean_text.splitlines()
        if line.strip()
    )

    return comment_text