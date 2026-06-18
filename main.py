# Packages

from db import add_job
import os
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

#debug
print(today)

text = (f"+ {companyName} -- {positionName} -- {jobCity} -- {jobState} -- {jobStatus[0]} -- {today}\n")

# Debug
print(text)

# writes into markdown file
with open("Job-Application-List.md", "a") as f:
    f.write(text)

text = (f"{companyName}-{positionName}-{today}")

with open(f"description/{text}", "w") as f:
    f.write(jobDescription)


add_job(companyName, positionName, jobCity, jobState, jobSite, jobStatus, jobDescription, today)

