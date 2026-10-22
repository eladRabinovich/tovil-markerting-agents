import asyncio
import json
import base64
import gzip
import csv
from playwright.async_api import async_playwright

STREET_URL = "https://www.nadlan.gov.il/?view=street&id=62000210&page=deals"
OUTPUT_FILE = "nadlan_deals.csv"


def decode_response_body(text: str):
    """The API returns gzip+base64 encoded JSON."""
    try:
        raw = base64.b64decode(text)
        return json.loads(gzip.decompress(raw).decode("utf-8"))
    except Exception:
        try:
            return json.loads(text)
        except Exception:
            return None


async def main():
    all_items = []
    page_count = 0

    async with async_playwright() as p:
        # headless=False to pass reCAPTCHA Enterprise detection
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        async def handle_response(response):
            nonlocal page_count
            if "api.nadlan.gov.il/deal-data" in response.url:
                try:
                    text = await response.text()
                    data = decode_response_body(text)
                    if data and data.get("statusCode") == 200:
                        items = data.get("data", {}).get("items", [])
                        total_rows = data.get("data", {}).get("total_rows", 0)
                        total_pages = data.get("data", {}).get("total_page", 0)
                        page_count += 1
                        all_items.extend(items)
                        print(f"Page {page_count}/{total_pages}: got {len(items)} items "
                              f"(total collected: {len(all_items)}/{total_rows})")
                        # Print first item's keys so we know the schema
                        if page_count == 1 and items:
                            print(f"Fields: {list(items[0].keys())}")
                except Exception as e:
                    print(f"Response error: {e}")

        page.on("response", handle_response)

        print("Loading page (browser window will open)...")
        await page.goto(STREET_URL)

        # Wait for the first data load
        await page.wait_for_timeout(6000)

        # Now click through all pages using the "הבא" (next) button
        while True:
            try:
                next_btn = await page.query_selector("button#next, button.nextBtn")
                if not next_btn:
                    print("No next button found — done.")
                    break

                # Check if button is visible/enabled
                is_visible = await next_btn.is_visible()
                is_enabled = await next_btn.is_enabled()
                if not is_visible or not is_enabled:
                    print("Next button is hidden/disabled — done.")
                    break

                # Get current page indicator before clicking
                page_indicator = await page.text_content("li.paginate")
                print(f"  Clicking next from: {page_indicator}")

                await next_btn.click()
                await page.wait_for_timeout(3000)

            except Exception as e:
                print(f"Pagination stopped: {e}")
                break

        print(f"\nDone. Collected {len(all_items)} total deals.")
        await browser.close()

    if not all_items:
        print("No data collected. The page may require manual interaction.")
        return

    # Save to CSV
    keys = list(all_items[0].keys())
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_items)

    print(f"Saved to {OUTPUT_FILE}")

    # Also save raw JSON
    with open("nadlan_deals.json", "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)
    print("Also saved raw JSON to nadlan_deals.json")


asyncio.run(main())
