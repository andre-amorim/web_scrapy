# Universal Web Scraper (Codelabs Edition)

A robust, "bulletproof" tool to scrape Google Codelabs (and other websites) into clean PDF or Markdown files.

## Features

- **Specialized Codelabs Support:** Automatically unhides all steps, removes navigation/drawers, and formats for print/PDF.
- **Generic Fallback:** Works on any website (basic print view).
- **Playwright Engine:** Uses a real browser for perfect rendering of Single Page Apps (SPAs).
- **Extensible:** Uses a Strategy pattern to easily add new site-specific logic.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (Fast Python package manager)

## Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd codelabs-scraper

# 2. Install dependencies
uv sync

# 3. Install Playwright browsers
uv run playwright install chromium
```

## Usage

### Generate PDF (Default)
```bash
uv run codelabs-scraper https://codelabs.developers.google.com/instavibe-adk-multi-agents/instructions#0 --output tutorial.pdf
```

### Generate Markdown
```bash
uv run codelabs-scraper https://codelabs.developers.google.com/instavibe-adk-multi-agents/instructions#0 --format md --output tutorial.md
```

### Generic Site (PDF)
```bash
uv run codelabs-scraper https://example.com --output example.pdf
```

## Architecture

The project is structured to be easily extensible:

- `src/codelabs_scraper/core/strategies.py`: Base class for scraping strategies.
- `src/codelabs_scraper/sites/`: Contains site-specific strategies.
  - `codelabs.py`: Logic for Google Codelabs.
  - `generic.py`: Fallback logic.

To add a new site (e.g., Medium):
1. Create `src/codelabs_scraper/sites/medium.py`.
2. Implement a class inheriting from `ContentStrategy`.
3. Add it to the priority list in `src/codelabs_scraper/main.py`.
