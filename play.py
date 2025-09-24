import csv
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def main():
    # Read header CSV
    with open("header2.csv", 'a') as header:
        header_reader = csv.reader(header)
        skills = ['laravel']  # Fetch first row as skills
    print(type(skills))

    # Prepare CSV writer for output
    with open("skillsFreelancerFinal.csv", "a", newline='') as f:
        csv_writer = csv.writer(f)
        elements_checked = []

        async with async_playwright() as p:
            # Launch browser in headless mode with required settings
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://www.freelancer.com/jobs/?results=100")
            await page.set_viewport_size({"width": 1366, "height": 728})

            # Close the project banner
            await page.wait_for_selector("#post-project-banner-close path")
            await page.click("#post-project-banner-close path")

            # Select all job results
            await page.click(".Radio-label:nth-child(4)")

            for skill in skills:
                print(f"Processing skill: {skill}")
                await page.fill("#job-search-selector-Skills-autofill-input", skill)
                await page.wait_for_selector(".AutofillDropdown-dropdown-item:nth-child(1)")
                await page.click(".AutofillDropdown-dropdown-item:nth-child(1)")

                # Parse page source to retrieve total results
                html = await page.content()
                soup = BeautifulSoup(html, 'html.parser')
                div = soup.find(id="total-results")
                number_total = int(div.text.replace(',', ''))
                n = 100 if number_total > 10000 else number_total // 100

                # Process pagination
                for i in range(2, n + 1):
                    await page.click("(//a[contains(@href, '#')])[9]")
                    await page.wait_for_timeout(7000)  # Wait for page load

                    # Parse HTML for skills
                    html = await page.content()
                    soup = BeautifulSoup(html, 'html.parser')
                    tags = soup.findAll("div", {"class": "JobSearchCard-primary-tags"})

                    for tag in tags:
                        list_el = [child.text for child in tag.findChildren()]
                        if not any(item in list_el for item in elements_checked):
                            csv_writer.writerow(list_el)
                            print(list_el)

                # Toggle skill filter for next iteration
                await page.click("(//a[contains(@href, '#')])[4]")
                elements_checked.append(skill)

            await browser.close()

# Run the Playwright script asynchronously
asyncio.run(main())
