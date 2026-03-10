"""Manages the jobs database and streamlines SQL queries"""

import sqlite3


#SEARCHING

def get_jobs_array():
    return sql.execute("SELECT * FROM jobs").fetchall()


def get_jobs_count():
    return len(get_jobs_array())


# Searches the database for a job with the same link (as this should be unique and we can't use ID to compare to something not in the db)
def job_in_db(URL : str):
    job = sql.execute("SELECT * FROM jobs WHERE link=?",(URL,))
    if (job.fetchone() is None):
        return False
    else:
        return True


# Need to convert to PHP and run on the server rather than here
def search(query : str):
    query = query.lower().strip().split()
    results = []
    for q in query:
        # Add Try Except here
        q = f'%{q}%'
        result = sql.execute("SELECT * FROM jobs WHERE title LIKE ?",(q,)).fetchall()
        if (result is not None):
            results.append(result)
    
    return results

#CHANGING

def remove_job(job_id : int):
    sql.execute("DELETE FROM jobs WHERE id=?", (int(job_id),))
    database.commit()


def add_job(title : str, company : str, link : str, date : str, location : str):
    sql.execute("INSERT INTO jobs(title, company, link, date, location) VALUES (?, ?, ?, ?, ?)", (title, company, link, date, location))
    database.commit()


def add_jobs(job_array : list):
    for job in job_array:
        sql.execute("INSERT INTO jobs(title, company, link, date, location) VALUES (?, ?, ?, ?, ?)", (job['title'], job['company'], job['link'], job['date'], job['location']))

    database.commit()


# Returns number of jobs added (1 or 0)
# NOTE: This is rather slow if used within a for loop as it commits for each job.
# Consider implementing a version that takes an array of job dicts instead to commit all at once
def add_job_if_new(title : str, company : str, link : str, date : str, location : str):
    if (not job_in_db(link)):
            add_job(title, company, link, date, location)
            return 1
    return 0


# Returns number of jobs added
def add_jobs_if_new(job_array : list):
    count = 0

    for job in job_array:
        if (not job_in_db(job['link'])):
            sql.execute("INSERT INTO jobs(title, company, link, date, location) VALUES (?, ?, ?, ?, ?)", (job['title'], job['company'], job['link'], job['date'], job['location']))
            count+= 1

    database.commit()

    return count


database = sqlite3.connect("jobs.db")
sql = database.cursor()
#Create the database if not found
#ID, Job Title, Company, Link, Date (yyyy-mm-dd)
# NOTE: This will create the database in the cwd of the command line. It's important then that this script is run from that 'database' directory for proper organisation 
# NOTE: Use cron job or build this script as an .exe and use task scheduler or command line to automatically update the database
sql.execute("CREATE TABLE IF NOT EXISTS jobs(id INTEGER PRIMARY KEY, title TEXT, company TEXT, link TEXT, date TEXT, location TEXT)")