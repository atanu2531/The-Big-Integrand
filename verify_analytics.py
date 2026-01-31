import asyncio
from playwright.async_api import async_playwright

async def run_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            # Streamlit usually takes a few seconds to load
            print("Connecting to Streamlit app at http://localhost:8501...")
            await page.goto("http://localhost:8501", timeout=60000)

            # Check for the title
            title_content = await page.title()
            print(f"Page Title: {title_content}")

            # Check for the main header
            header = await page.wait_for_selector("h1", timeout=10000)
            header_text = await header.inner_text()
            print(f"Header: {header_text}")

            if "Senior Data Scientist" in header_text:
                print("Verification Successful: Title found.")
            else:
                print("Verification Failed: Title not found.")
                exit(1)

            # Check for metrics (they are usually in [data-testid="stMetricValue"])
            metrics = await page.query_selector_all('[data-testid="stMetricValue"]')
            if len(metrics) > 0:
                print(f"Found {len(metrics)} metrics on the dashboard.")
            else:
                print("Warning: No metrics found. Data might not be loaded yet.")

        except Exception as e:
            print(f"An error occurred during verification: {e}")
            exit(1)
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_test())
