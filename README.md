# Webscraper

# Tools
Here's what each tool is used for:

- Python 3.9 download - programming the logic.
- AstraDB sign up - highly perfomant and scalable database service by DataStax. AstraDB is a Cassandra NoSQL Database. Cassandra is used by Netflix, Discord, Apple, and many others to handle astonding amounts of data.
- Selenium docs - an automated web browsing experience that allows:
   - Run all web-browser actions through code
   - Loads JavaScript heavy websites
   - Can perform standard user interaction like clicks, form submits, logins, etc.
- Requests HTML docs - we're going to use this to parse an HTML document extracted from Selenium
- Celery docs - Celery providers worker processes that will allow us to schedule when we need to scrape websites. We'll be using redis as our task queue.
- FastAPI docs - as a web application framework to Display and monitor web scraping results from anywhere


Scraping How to scrape and parse data from nearly any website with Selenium & Requests HTML.
Data models how to store and validate data with cassandra-driver, pydantic, and AstraDB.
Worker & Scheduling how to schedule periodic tasks (ie scraping) integrated with Redis & AstraDB

# Installation
- Install Selenium & Chromedriver - setup guide
- Install Redis - setup guide
- Create a virtual environment (optional) & install dependencies (required)
- Setup an account with DataStax
- Create your first AstraDB and get API credentials
- Use cassandra-driver to verify your connection to AstraDB
