from ..core.strategies import ContentStrategy
from playwright.sync_api import Page


class GenericStrategy(ContentStrategy):
    def can_handle(self, url: str) -> bool:
        return True

    def prepare_page(self, page: Page) -> None:
        # Basic generic cleanup
        page.evaluate("""
            () => {
                // Try to hide cookie banners if obvious (this is brittle but helpful)
                const commonBannerSelectors = [
                    '[id*="cookie"]', '[class*="cookie"]',
                    '[id*="consent"]', '[class*="consent"]'
                ];
                // Be conservative, only hide if fixed position (floating)
                commonBannerSelectors.forEach(sel => {
                     document.querySelectorAll(sel).forEach(el => {
                         const style = window.getComputedStyle(el);
                         if (style.position === 'fixed' || style.position === 'sticky') {
                             el.style.display = 'none';
                         }
                     });
                });
            }
        """)
