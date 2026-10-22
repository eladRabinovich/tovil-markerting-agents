import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.nadlan.gov.il/?view=street&id=62000210&page=deals")
        await page.wait_for_timeout(6000)

        # Dump pagination HTML
        pagination_html = await page.evaluate("""
            () => {
                // Try various common pagination containers
                const selectors = [
                    '.pagination', '[class*="pagination"]', '[class*="pager"]',
                    'nav', '.page-nav', '[class*="page"]'
                ];
                for (const sel of selectors) {
                    const el = document.querySelector(sel);
                    if (el) return { selector: sel, html: el.outerHTML.substring(0, 3000) };
                }
                return { selector: 'none', html: document.body.innerHTML.substring(0, 5000) };
            }
        """)
        print("=== Pagination HTML ===")
        print(f"Found via: {pagination_html['selector']}")
        print(pagination_html['html'])

        # Also list all buttons on page
        buttons = await page.evaluate("""
            () => Array.from(document.querySelectorAll('button, a')).map(el => ({
                tag: el.tagName,
                text: el.innerText.trim().substring(0, 50),
                cls: el.className,
                disabled: el.disabled || el.getAttribute('disabled'),
                href: el.href || ''
            })).filter(b => b.text)
        """)
        print("\n=== All buttons/links ===")
        for b in buttons[:30]:
            print(b)

        await browser.close()

asyncio.run(main())
