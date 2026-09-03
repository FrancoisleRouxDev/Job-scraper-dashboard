from flask import Blueprint, render_template, request
from app.db import get_connection
from app.scraper import scrape_pnet, save_jobs

main = Blueprint("main", __name__)

@main.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor()

    search = request.args.get("search", "")
    location = request.args.get("location", "")

    query = "SELECT * FROM jobs WHERE 1=1"
    params = []

    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")

    if location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")

    query += " ORDER BY date_posted DESC"
    cursor.execute(query, params)
    jobs = cursor.fetchall()
    conn.close()

    return render_template("index.html", jobs=jobs, search=search, location=location)

@main.route("/scrape")
def scrape():
    jobs = scrape_pnet()
    if jobs:
        save_jobs(jobs)
    return index()