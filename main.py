# Packages

import os
import sqlite3
from datetime import date

# Sets workign directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Variables
companyName = input("Company: ")
positionName = input("Position: ")
jobCity = input("City: ")
jobState = input("State: ")
jobSite = input("Is this Position hybrid, on-site, or Remote: ")
jobStatus = ["In Progress", "Ghosted", " Rejected"]
jobDescription = input("Enter Description: ")
today = str(date.today())
spacingBar = " -- "

print(today)

text = (f"+ {companyName} -- {positionName} -- {jobCity} -- {jobState} -- {jobStatus[0] -- {today}")

print(text)

# writes into markdown file
with open("Job-Application-List.md", "a") as f:
    f.write(text)

text = (f"{companyName}-{positionName}-{today}")

with open(f"description/{text}", "w") as f:
    f.write(jobDescription)



# SQL selection
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
    description TEXT,
    status TEXT CHECK(status IN ('In Progress', 'Ghosted', 'Rejected')),
    date TEXT
)
""")


cur.execute(
    "INSERT INTO application (company, position, city, state, site, description, status, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    (companyName, positionName, jobCity, jobState, jobSite, jobDescription, jobStatus[0], today)
)

con.commit()
con.close()
