import sqlite3

def add_job(
    companyName, 
    positionName,
    jobCity,
    jobState,
    jobSite,
    jobStatus,
    jobDescription,
    today,
):

# SQL selection
    con = sqlite3.connect("tracker.db")
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications(
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
        "INSERT INTO applications (company, position, city, state, site, description, status, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (companyName, positionName, jobCity, jobState, jobSite, jobDescription, jobStatus[0], today)
    )

    con.commit()
    con.close()

pass
