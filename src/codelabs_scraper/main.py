import typer
from rich.console import Console
from pathlib import Path
from playwright.sync_api import sync_playwright
import markdownify
from .core.strategies import ContentStrategy
from .sites.codelabs import CodelabsStrategy
from .sites.generic import GenericStrategy

app = typer.Typer()
console = Console()


def get_strategy(url: str) -> ContentStrategy:
    # Priority list
    strategies = [CodelabsStrategy()]
    for s in strategies:
        if s.can_handle(url):
            return s
    return GenericStrategy()


@app.command()
def scrape(
    url: str,
    output: Path = typer.Option(
        ..., help="Path to save the output (e.g. tutorial.pdf or tutorial.md)"
    ),
    format: str = typer.Option("pdf", help="Output format: 'pdf' or 'md'"),
    headless: bool = True,
):
    """
    Scrape a website (optimized for Codelabs) and save as PDF or Markdown.
    """
    strategy = get_strategy(url)
    console.print(
        f"[bold green]Using strategy:[/bold green] {strategy.__class__.__name__}"
    )

    with sync_playwright() as p:
        console.print(f"Launching browser (Headless: {headless})...")
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        console.print(f"Navigating to {url}...")
        page.goto(url, wait_until="networkidle")

        console.print("Preparing page content...")
        strategy.prepare_page(page)

        # Small buffer for JS rendering
        page.wait_for_timeout(2000)

        if format.lower() == "pdf":
            console.print(f"Generating PDF to [bold]{output}[/bold]...")
            # emulating print media helps sometimes
            page.emulate_media(media="print")
            page.pdf(path=output, format="A4", print_background=True)

        elif format.lower() == "md":
            console.print(f"Converting to Markdown to [bold]{output}[/bold]...")
            html = strategy.get_html_for_markdown(page)
            md_content = markdownify.markdownify(
                html, heading_style="ATX", strip=["script", "style"]
            )
            output.write_text(md_content, encoding="utf-8")

        console.print("[bold green]Done![/bold green]")
        browser.close()


if __name__ == "__main__":
    app()
