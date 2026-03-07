GENERAL

Game Job Scraper is intended to be an example of how to create a webscraper in Python. In this specific example it's used to aggregate jobs from various job boards in the game industry. 

Instead of searching through numerous boards for updates, it allows users to view a single hub of jobs from a collection of studios. Whilst this specific repository if focused on the webscraping aspect, I've included a barebones example of how this data can be presented as a website (www.mattmuller.website).

AUTOMATION

In addition, jobscraper.py can be ran as a background process and will send a push notification if it finds any new jobs to promptly update users of new openings, allowing them to get a headstart on their application. In this day and age, being the 'first on the stack' can mean the difference between success and failure when hiring managers need to view hundreds if not thousands of applications. 

My method for automation is through the task scheduler. I use pyinstaller to convert jobscraper.py to an .exe (making sure I include all dependencies) and then schedule the task to trigger hourly, updating my database each time and sending a push notification if it finds anything.
