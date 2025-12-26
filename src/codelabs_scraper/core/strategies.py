from abc import ABC, abstractmethod
from playwright.sync_api import Page
import markdownify


class ContentStrategy(ABC):
    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """Returns True if this strategy can handle the given URL."""
        pass

    @abstractmethod
    def prepare_page(self, page: Page) -> None:
        """Modifies the page in-place (via JS) to be ready for printing/exporting."""
        pass

    def get_html_for_markdown(self, page: Page) -> str:
        """Returns the HTML string best suited for Markdown conversion."""
        return page.content()
