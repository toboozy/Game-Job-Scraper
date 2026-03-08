from bs4 import BeautifulSoup
import requests
from win11toast import notify
import database.database_manager as db
import formatter as f
import json

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

GAMELOFT = {'URL' : "https://www.gameloft.com/jobs",
            'title_element' : 'a', 
            'title_attrs' : {'class': '_row_b9eb0_121'},
            'fetch-URL' : 'https://wmt-api.gameloft.com/api/gameloft/smart-recruiter-jobs?&visible=1&page=1&limit=999&lang=en'
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
        if is_valid_job(job.string):
                results.append(job)

    return results


# Checks the job against the KEYWORD filter
def is_valid_job(job_title : str):
    for keyword in KEYWORDS:
            if (keyword in job_title.lower().strip()):
                 return True
            else:
                 return False


# METHOD 1: READING HTML DATA
# This method uses the HTML elements to determine what information it needs to collect
# By inspecting the websites HTML, we can find the names of the elements and classes for our desired information
# For example, the job titles all use a Div element with a class of text-block-28 (and importantly are the ONLY elements that do so)
# By using find_all with BeautifulSoup, I recieve a copy of all elements matching that description, giving me a copy of all job titles
def scrape_work_with_indies():

    work_with_indies = get_soup(WORK_WITH_INDIES['URL'])

    job_titles = work_with_indies.find_all(WORK_WITH_INDIES['title_element'], attrs=WORK_WITH_INDIES['title_attrs'])

    filtered_jobs = filter_jobs(job_titles)

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
        
    return db.add_jobs_if_new(job_array)
     

# METHOD 2: READING JSON FROM FETCH REQUEST
# This time I'm going to show an example of using JSON data to scrape a website.
# By locating the fetch/XHR request (under network tab of inspect), 
# we can use the request URL with our own modified queries to directly access the data the job board is using

# I'm using this method here because Gameloft doesn't show all jobs on a single page, something referred to as pagination
# In addition, they don't display the get request in the URL (meaning we can't just change the URL to get the next page)
# There are a few ways around this, like Selenium to click the next button, but I believe intercepting the 
def scrape_gameloft():
    
    # NOTE: it's not required to use beautiful soup here as the request should return JSON.
    # I'm using it so that if something breaks I have fewer places to check.
    gameloft = get_soup(GAMELOFT['fetch-URL'])

    try:
        gameloft_json = json.loads(gameloft.string)
    except:
        print(f"Unable to parse JSON from {GAMELOFT['fetch-URL']}")
        return

    job_array = []

    for job in gameloft_json['data']:
        if (is_valid_job(job['name'])):
            job_array.append({
                  'title' : job['name'],
                  'company' : 'Gameloft',
                  'link' : job['postingUrl'],
                  'date' : job['releasedDate'][0:10],
                  'location' : job['location']})
             
    return db.add_jobs_if_new(job_array)


# Fetches all job boards and sends push notification if anything is found
def refresh_job_board():
    new_job_count = scrape_work_with_indies()
    new_job_count += scrape_gameloft()
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