from ..core.strategies import ContentStrategy
from playwright.sync_api import Page


class CodelabsStrategy(ContentStrategy):
    def can_handle(self, url: str) -> bool:
        return "codelabs.developers.google.com" in url or "codelabs.google.com" in url

    def prepare_page(self, page: Page) -> None:
        # 1. Wait for content
        page.wait_for_selector("google-codelab-step")

        # 2. Inject CSS/JS to transform SPA to Single Print Page
        page.evaluate("""
            () => {
                // FORCE RESET: The parent container often has position: fixed/absolute and height: 100%
                // which clips content when we unhide steps. We must bust it out.
                
                const codelab = document.querySelector('google-codelab');
                if (codelab) {
                    codelab.removeAttribute('hidden');
                    codelab.style.display = 'block';
                    codelab.style.height = 'auto';
                    codelab.style.overflow = 'visible';
                    codelab.style.position = 'static';
                }

                // Unhide all steps and make them flow naturally
                const steps = document.querySelectorAll('google-codelab-step');
                steps.forEach(step => {
                    step.removeAttribute('hidden');
                    step.style.display = 'block';
                    step.style.visibility = 'visible';
                    step.style.position = 'static';  // Critical: defaults to absolute in some views
                    step.style.height = 'auto';
                    step.style.overflow = 'visible';
                    
                    // Add spacing
                    step.style.marginBottom = '40px';
                    step.style.borderBottom = '1px solid #ccc';
                    step.style.paddingBottom = '20px';
                });

                // Hide layout junk
                const selectorsToHide = [
                    '#drawer', 
                    '#controls', 
                    '.site-header',
                    '#feedback-survey', 
                    '.survey-container',
                    'div[class*="fab"]' // Floating action buttons
                ];
                
                selectorsToHide.forEach(sel => {
                    const els = document.querySelectorAll(sel);
                    els.forEach(el => el.style.display = 'none');
                });

                // Reset margins on main content to use full width
                const main = document.querySelector('#main');
                if (main) {
                    main.style.marginLeft = '0';
                    main.style.padding = '0 20px';
                    main.style.maxWidth = '100%';
                    main.style.height = 'auto';
                    main.style.overflow = 'visible';
                }
            }
        """)

    def get_html_for_markdown(self, page: Page) -> str:
        # Return only the steps content concatenation
        return page.evaluate("""
            () => {
                 const steps = Array.from(document.querySelectorAll('google-codelab-step'));
                 return steps.map(s => `<h2>${s.getAttribute('label') || ''}</h2>` + s.innerHTML).join('\\n<hr>\\n');
            }
        """)
