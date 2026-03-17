# Game Job Scraper
A collection of automatically aggregated programming jobs for game developers

#### Description:

Game Job Scraper is an example of how to create a webscraper using Python, SQL, and Beautiful Soup. 

In this specific example, I've used it to aggregate posts from various job boards in the game industry, however webscraping can be used to automate the collection of any data from any website, making it an invaluable skill for the data hoarder. 

I (currently) showcase two methods of webscraping: 

1. Reading HTML

In this method, the webscraper reads the HTML document and uses Beautiful Soup to filter it. By determining the unique Element, Class, and other attributes of our desired information to scrape, we can store the element and access it's attributes with Beautiful Soup.

2. Reading JSON

At times, a website will obfuscate information that makes reading HTML more difficult. For example, many websites include pagination that limits the information present in the HTML. To get around this, we can access the fetch request directly and input our own paramaters to recieve the JSON data used to populate the website. 

Whilst this specific repository if focused on the webscraping aspect, I've included a barebones example of how this data can be presented as a website (www.mattmuller.website/jobs).

Jobscraper.py can also be ran as a background process and will send a push notification if it finds any new jobs. In this day and age, being the 'first on the stack' can mean the difference when hiring managers need to view hundreds if not thousands of applications. 

My method for automation is through the task scheduler. I use pyinstaller to convert jobscraper.py to an .exe (making sure I include all dependencies) and then schedule the task to trigger hourly, updating my database each time and sending a push notification if it finds anything.
