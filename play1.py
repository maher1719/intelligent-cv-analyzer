import csv
import asyncio
import time
from playwright.async_api import Playwright, async_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import aiofiles

async def fetch_skill_page_data(page, skill, csv_writer):
    """Fetches data from a skill-specific page and writes tags to the CSV."""
    try:
        page_source = await page.content()
        html = BeautifulSoup(page_source, 'lxml')
        tags = html.findAll("div", {"class": "JobSearchCard-primary-tags"})
        for tag in tags:
            list_el = [child.text for child in tag.findChildren()]
            await csv_writer.writerow(list_el)
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

async def scrape_skill_data(skill, page, csv_writer, skill_count, total_skills, start_time):
    """Scrapes data for a given skill, navigating through pages if available."""
    skill=skill.replace(" ","-")
    await page.goto(f"https://www.freelancer.com/jobs/{skill}/?status=all&results=100")
    print(f"https://www.freelancer.com/jobs/{skill}/?status=all&results=100")
    
    page_num = 0
    try:
        # Attempt to get the inner text of the span with id 'total-results'
        total_results_text = await page.locator("#total-results").inner_text()
        # Convert the result to an integer, removing commas if they exist
        total_results = int(total_results_text.replace(",", "").strip())
        
    except Exception as e:
        print(f"Element not found or error occurred: {e}")
        # Return a default value or None if you want to indicate failure
        return None
        
        # Remove commas and convert to integer
    total_results = int(total_results_text.replace(',', '').strip())
    max_pages= total_results//100
    print("max pages",max_pages)
    while page_num<max_pages:
        print(f"Scraping '{skill}', page {page_num} max pages {max_pages} ")
        await fetch_skill_page_data(page, skill, csv_writer)
        page_num += 1
        progress = skill_count / total_skills * 100
        elapsed_time = time.time() - start_time
        estimated_total_time = (elapsed_time / progress) * 100 if progress > 0 else 0
        time_remaining = estimated_total_time - elapsed_time
        print(f"Global progress: {progress:.2f}% | Estimated time remaining: {time_remaining / 60:.2f} minutes")
        
        if not await navigate_to_next_page(page):
            break  # Exit loop if no more pages are available

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()
        
        async with aiofiles.open("skillsFreelancerFinal.txt", mode="a", newline='') as f:
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
