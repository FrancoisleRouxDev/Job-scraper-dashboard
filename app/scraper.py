import requests
from bs4 import BeautifulSoup
from datetime import date
import sqlite3
from app.db import get_connection

def scrape_pnet():
    url = "https://www.pnet.co.za/en/job/result/?what=junior+developer&where=gauteng"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []

    listings = soup.find_all("div", class_="job-card")

    for listing in listings:
        title = listing.find("h2")
        company = listing.find("span", class_="company-name")
        location = listing.find("span", class_="location")
        link = listing.find("a", href=True)

        jobs.append({
            "title": title.text.strip() if title else "N/A",
            "company": company.text.strip() if company else "N/A",
            "location": location.text.strip() if location else "N/A",
            "date_posted": str(date.today()),
            "url": "https://www.pnet.co.za" + link["href"] if link else "N/A",
            "source": "PNet"
        })

    return jobs

def save_jobs(jobs):
    conn = get_connection()
    cursor = conn.cursor()

    for job in jobs:
        cursor.execute('''
            INSERT INTO jobs (title, company, location, date_posted, url, source)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (job["title"], job["company"], job["location"], job["date_posted"], job["url"], job["source"]))

    conn.commit()
    conn.close()
    print(f"Saved {len(jobs)} jobs to database.")