import pyfiglet
from rich.console import Console
from rich.panel import Panel
from file_gen.file_handler import create_file
from db.llm_cache import get_tags_from_domain
from utils.get_question import map_question, create_table
from utils.get_all_info import get_question
from utils.get_available_languages import show_language
from utils.map_lang import map_lang
from utils.display import clean_text
import subprocess
console = Console()


def show_banner():
    banner = pyfiglet.figlet_format("LazyLeetCode 🥱")
    console.print(f"[bold white]{banner}[/bold white]")
    console.print(Panel("[yellow]🦥 LeetCode problems tailored to your domain[/yellow]",
                        border_style="blue"))


def prompt(msg: str) -> str:
    while True:
        val = input(msg).strip()
        if val:
            return val
        console.print("[red]Input cannot be empty. Please try again.[/red]\n")


def main():
    show_banner()

    field = prompt("Tell about the field you are interested in:\n").lower()
    if field is None:
        print("[bold yellow]Please enter correct domain")
        return
    # Step 1 — Get tags from LLMadsfsdg
    try:
        with console.status("[yellow]Fetching tags and getting related questions...[/yellow]"):
            related_tags = get_tags_from_domain(domain=field)
    except Exception as e:
        console.print(f"[red]Failed to fetch tags for '{field}': {e}[/red]")
        return
    console.print(f"[green]Tags:[/green] {', '.join(related_tags)}\n")

    # Step 2 — Filter questions
    try:
        question_list = map_question(tag_list=related_tags)
        create_table(question_list=question_list)
    except Exception as e:
        console.print(f"[red]Failed to fetch questions: {e}[/red]")
        return

    # Step 3 — Select question
    question_id = prompt("\nSelect a question number you want to solve:\n")
    try:
        question_info = get_question(question_no=question_id)
    except Exception as e:
        console.print(f"[red]Could not fetch question '{question_id}': {e}[/red]")
        return

    # Step 4 — Select language
    show_language(question_info=question_info, question_no=question_id)
    language_input = prompt("Choose a language to solve the question:\n").strip()
    try:
        extension, comment_syntax = map_lang(lang=language_input)
    except Exception as e:
        console.print(f"[red]Unsupported language '{language_input}': {e}[/red]")
        return

    # Step 5 — Generate file
    raw_description = question_info['description']
    clean_desc = clean_text(response_with_html_tags=raw_description, comment_tag=comment_syntax)
    question_title = question_info['slug']
    difficulty = question_info['difficulty']
    code_str = question_info['code'].get(language_input)

    if code_str is None:
        console.print(f"[red]No code template found for '{language_input}'. Try a different language.[/red]")
        return

    try:
        with console.status("[yellow]Generating your file...[/yellow]"):
            file_path = create_file(
                file_name=question_title,
                mapped_lang=extension,
                difficulty=difficulty,
                user_question=question_id,
                code=code_str,
                cmt=comment_syntax,
                desc=clean_desc
            )
        console.print(f"\n[bold green]File created successfully for '{question_title}' in {language_input}![/bold green]")
        console.print("[bold green]Happy Coding! 🦥[/bold green]\n")
        try:
            console.print(file_path)
            subprocess.run(["code",file_path],shell=True)
        except Exception as e:
            console.print(f"[bold lightblue][ERROR]: could not open VS CODE due to: << {e} >> Still you can manually open a solve the problem")
    except Exception as e:
        console.print(f"[red]Failed to create file: {e}[/red]")


if __name__ == "__main__":
    main()