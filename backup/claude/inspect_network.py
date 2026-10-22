import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        async def handle_response(response):
            url = response.url
            if "api.nadlan.gov.il/deal-data" in url:
                try:
                    status = response.status
                    headers = dict(response.headers)
                    text = await response.text()
                    print(f"\n=== deal-data response (status {status}) ===")
                    print(f"Content-Type: {headers.get('content-type', 'N/A')}")
                    print(f"Body (first 2000 chars): {text[:2000]}")
                except Exception as e:
                    print(f"Error reading response: {e}")

        page.on("response", handle_response)

        print("Loading page...")
        await page.goto("https://www.nadlan.gov.il/?view=street&id=62000210&page=deals")
        await page.wait_for_timeout(8000)

        await browser.close()

asyncio.run(main())
