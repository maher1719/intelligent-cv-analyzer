from playwright.sync_api import sync_playwright
import csv
import re
import time

# Constants
JOB = "Javascript Developer"
CSV_FILE = "jobs.csv"
URL = "https://www.careerbuilder.com/"
PAGE_LIMIT = 26  # Define how many pages you want to scrape
WAIT_TIME = 3  # Adjust wait time as needed

# Initialize CSV file
with open(CSV_FILE, "a", newline='', encoding='utf-8') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["Job Title", "Description"])  # Header row

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)  # Set to True to run in headless mode
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the website
        page.goto(URL)
        time.sleep(WAIT_TIME)  # Allow time for the page to load

        # Input job search keyword
        page.fill('input#Keywords', JOB)
        page.press('input#Keywords', 'Enter')
        time.sleep(WAIT_TIME)

        try:
            page_number = 1

            while page_number <= PAGE_LIMIT:
                print(f"Scraping page {page_number}...")

                # Locate job postings on the current page
                job_cards = page.query_selector_all('.data-results-content-parent .data-results-content')
                if not job_cards:
                    print("No job cards found. Ending scrape.")
                    break

                for job_card in job_cards:
                    try:
                        job_card.click()
                        time.sleep(WAIT_TIME)  # Allow job details to load

                        # Extract job description
                        job_description = page.query_selector('#jdp_description')
                        description_text = job_description.inner_text() if job_description else "No description found."
                        cleaned_text = re.sub(r'[^a-zA-Z0-9.\d\s]', '', description_text).replace("\n", " ").strip()

                        # Write to CSV
                        csv_writer.writerow([JOB, cleaned_text])
                        print(f"Job scraped: {JOB}")

                        # Go back to the job list page
                        page.go_back()
                        time.sleep(WAIT_TIME)

                    except Exception as e:
                        print(f"Error scraping job card: {e}")
                        continue

                # Go to the next page if available
                next_button = page.query_selector('//div[3]/div/div[3]/a')
                if next_button:
                    next_button.click()
                    time.sleep(WAIT_TIME)
                    page_number += 1
                else:
                    print("No more pages to navigate.")
                    break

        except Exception as e:
            print(f"Error during scraping: {e}")

        finally:
            browser.close()
