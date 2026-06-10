# Packages

import sqlite3
from datetime import date

# Variables
companyName = input("Company: ")
positionName = input("Position: ")
jobCity = input("City: ")
jobState = input("State: ")
jobSite = input("Is this Position hybrid, on-site, or Remote: ")
jobStatus = ["In Progress", "Ghosted", " Rejected"]
today = str(date.today())
spacingBar = " -- "

print(today)

text = ("+ " + today + spacingBar + companyName + spacingBar + positionName + spacingBar + jobCity + spacingBar + jobState + spacingBar + jobSite + spacingBar + jobStatus[0] + "\n")

print(text)

with open("Job-Application-List.md", "a") as f:
    f.write(text)



con = sqlite3.connect("tracker.db")

cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS application(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    position TEXT,
    city TEXT,
    state TEXT,
    site TEXT,
    status TEXT CHECK(status IN ('In Progress', 'Ghosted', 'Rejected')),
    date TEXT
)
""")


cur.execute(
    "INSERT INTO application (company, position, city, state, site, status, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
    (companyName, positionName, jobCity, jobState, jobSite, jobStatus[0], today)
)
con.commit()

res = cur.execute(
    "SELECT strftime('%Y-%m', date) AS month, COUNT(*) FROM application GROUP BY month"
)
for row in res.fetchall():
    print(row)

con.close()
