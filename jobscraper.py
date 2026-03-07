from bs4 import BeautifulSoup
import requests
from win11toast import notify
import database.database_manager as db
import formatter as f

#EXIT CODE
exit_code = 0

#FILTERS
KEYWORDS = ['programmer', 'c#', 'developer', 'engineer']

#WEBSITE SCRAPING CONFIGS
WORK_WITH_INDIES = {'URL':"https://www.workwithindies.com/", 
                        'title_element':'div', 'title_attrs':{'class':'text-block-28'},
                        'company_element':'div', 'company_attrs':{'class':'job-card-text bold'},
                        'date_element' : 'div', 'date_attrs' : {'class': 'posted'},
                        'location_element' : 'div', 'location_attrs' : {'class': 'tags location'}
                        }


# Returns some beautiful soup from the requested URL
def get_soup(URL : str):
    try:
        response = requests.get(URL, headers= {"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

    return BeautifulSoup(response.text, "html.parser")


# Loops through all jobs and checks if they're valid
def filter_jobs(job_titles : list):
    results = []
    for job in job_titles:
        if is_valid_job(job):
                results.append(job)

    return results


# Checks the job against the KEYWORD filter
def is_valid_job(job_title : str):
    for keyword in KEYWORDS:
            if (keyword in job_title.string.lower().strip()):
                 return True
            else:
                 return False


# Handles scraping jobs from 'Work with Indies'
# Returns the number of NEW jobs for our toast notification
def scrape_work_with_indies():

    work_with_indies = get_soup(WORK_WITH_INDIES['URL'])

    job_titles = work_with_indies.find_all(WORK_WITH_INDIES['title_element'], attrs=WORK_WITH_INDIES['title_attrs'])

    filtered_jobs = filter_jobs(job_titles)

    new_job_count = 0

    job_array = []

    for job in filtered_jobs:
        job_title = job.string
        job_link = f'{WORK_WITH_INDIES['URL']}{job.parent.parent['href']}'    
        job_company = job.find_previous_sibling(WORK_WITH_INDIES['company_element'],WORK_WITH_INDIES['company_attrs']).string

        #go deeper
        job_page = get_soup(job_link)
        # Two elements are used to display the date [0] = 'Posted' [1] = 'MONTH DD, YYYY' 
        job_date = job_page.find_all(WORK_WITH_INDIES['date_element'], WORK_WITH_INDIES['date_attrs'])[1].string
        # Convert the date to ISO8601
        job_date = f.date_ISO(job_date,'MM-DD-YYYY')
        job_location = job_page.find(WORK_WITH_INDIES['location_element'], WORK_WITH_INDIES['location_attrs']).string

        # Check if the job is already in our database and insert the job if we don't find it

        job_array.append({'title' : job_title,
                          'company' : job_company,
                          'link' : job_link,
                          'date' : job_date,
                          'location' : job_location})
        
    new_job_count = db.add_jobs_if_new(job_array)

    return new_job_count
    
    
# Background process that fetches all job boards and sends push notification if anything is found
def refresh_job_board():
    new_job_count = 0
    new_job_count += scrape_work_with_indies()
    if new_job_count != 0:
        notify(str(new_job_count) + " NEW JOBS FOUND", duration="short", scenario="reminder")


def main():
    global exit_code

    refresh_job_board()
    print(db.get_jobs_array())

    if (exit_code == 0):
         print('Jobscraper completed successfully.')
    else:
         print('Jobscraper completed with some errors.')


if __name__ == "__main__":
     main()