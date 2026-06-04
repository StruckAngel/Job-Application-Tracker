

companyName = input("Company: ")
positionName = input("Position: ")
cityState = input("City, State: ")
jobSite = input("Is this Position hybrid, on-site, or Remote: ")
jobStatus = ["In Progress", "Ghosted", " Rejcted"]
spacingBar = " -- "


text = ("- " + companyName + spacingBar + positionName + spacingBar + cityState + spacingBar + jobSite + spacingBar + jobStatus[0])

print(text)

with open("Job-Application-List.md", "a") as f:
    f.write(text)
