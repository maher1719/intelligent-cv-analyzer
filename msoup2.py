import csv
import asyncio
import time
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup

def write_to_csv(csv_writer, data):
    """Synchronously writes data to CSV."""
    csv_writer.writerow(data)

async def fetch_skill_page_data(page, skill, csv_writer):
    """Fetches data from a skill-specific page and writes tags to the CSV."""
    try:
        page_source = await page.content()
        html = BeautifulSoup(page_source, 'lxml')
        tags = html.findAll("div", {"class": "JobSearchCard-primary-tags"})
        for tag in tags:
            list_el = [child.text for child in tag.findChildren()]
            write_to_csv(csv_writer, list_el)
    except Exception as e:
        print(f"Error fetching data for {skill}: {e}")

async def navigate_to_next_page(page):
    """Navigates to the next page if the 'Next' button is available."""
    try:
        if await page.is_visible("//li[6]/a"):
            await page.click("//li[6]/a")
            await asyncio.sleep(1)  # Small delay for the page to load
            return True
    except PlaywrightTimeoutError:
        print("Next page button not found or not clickable.")
    return False

async def get_total_results(page):
    """Retrieves the total number of results available for the current skill."""
    try:
        total_results_text = await page.locator("#total-results").inner_text()
        total_results = int(total_results_text.replace(",", "").strip())
        return total_results
    except Exception as e:
        print(f"Error fetching total results: {e}")
        return 0

async def scrape_skill_data(skill, page, csv_writer, skill_count, total_skills, start_time):
    """Scrapes data for a given skill, navigating through pages if available."""
    await page.goto(f"https://www.freelancer.com/jobs/{skill}/?status=all&results=100")
    
    total_results = await get_total_results(page)
    total_pages = (total_results // 100) + (1 if total_results % 100 > 0 else 0)  # Calculate total pages based on results
    print(f"Total pages for '{skill}': {total_pages}")

    for page_num in range(total_pages):
        print(f"Scraping '{skill}', page {page_num + 1} of {total_pages}")
        await fetch_skill_page_data(page, skill, csv_writer)
        
        progress = (skill_count / total_skills * 100) + (page_num / total_pages * (100 / total_skills))
        elapsed_time = time.time() - start_time
        estimated_total_time = (elapsed_time / progress) * 100 if progress > 0 else 0
        time_remaining = estimated_total_time - elapsed_time
        print(f"Global progress: {progress:.2f}% | Estimated time remaining: {time_remaining / 60:.2f} minutes")
        
        if page_num < total_pages - 1:  # Navigate to next page if not the last page
            await navigate_to_next_page(page)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        with open("skillsFreelancerFinal.csv", mode="a", newline='') as f:
            csv_writer = csv.writer(f)
            with open("unique_skills.csv", 'r') as header:
                header_reader = csv.reader(header)
                skills = next(header_reader)

            start_time = time.time()
            for skill_count, skill in enumerate(skills, start=1):
                await scrape_skill_data(skill, page, csv_writer, skill_count, len(skills), start_time)

        await browser.close()

# Run the main function
asyncio.run(main())
