# Webscraper
Webscrapper is a tool built with FastAPI and Celery that allows you to scrape product data from Amazon. It uses Cassandra's AstraDB as the database and Redis as the message broker for Celery.

This project covers the following functionalities:

- Scraping: Scrapes and parses data from Amazon using Selenium and Requests HTML. Database schema can be modified to scrape nearly any website as well.

- Data Models: Stores and validates data using the cassandra-driver, pydantic, and AstraDB. 

- Worker & Scheduling: Schedules periodic tasks, such as scraping, by integrating Celery with Redis and AstraDB.

# Tools Used
This project utilizes the following tools:
- Python 3.9: Download Python 3.9 to program the logic of the application.

- AstraDB: Sign up for AstraDB, a highly performant and scalable NoSQL database service provided by DataStax. AstraDB is built on Cassandra, a popular NoSQL database used by companies like Netflix, Discord, Apple, and many others to handle vast amounts of data.

- Selenium: Refer to the Selenium documentation for automating web browsing. It allows you to execute web browser actions through code, load JavaScript-heavy websites, and perform standard user interactions such as clicks, form submits, logins, etc.

- Requests HTML: We will use Requests HTML to parse an HTML document extracted from Selenium.

- Celery: Celery provides worker processes that enable us to schedule website scraping tasks. We'll be using Redis as our task queue. Consult the Celery documentation for more information: https://docs.celeryq.dev/en/stable/

- FastAPI: FastAPI is used as the web application framework for displaying and monitoring web scraping results from anywhere. For details on how to use FastAPI, refer to the official documentation: https://fastapi.tiangolo.com/lo/
- 
# Installation 
1. Clone the git repository:
git clone https://github.com/Tochi-Onwuasoanya/Webscraper.git

2. Change into the project directory:
cd Webscraper

3. Install the dependencies:
pip install -r requirements.txt

4. Set up environemnt variables by creating a .env file in the project root directory and adding the following variables:
PROJ_NAME=Scraper App
ASTRA_DB_CLIENT_ID=your-astra-db-client-id
ASTRA_DB_CLIENT_SECRET=your-astra-db-client-secret
REDIS_URL=redis://localhost:6379/0

Replace your-astra-db-client-id and your-astra-db-client-secret with your actual Astra DB client ID and secret.

5. Start the FastAPI web server 
uvicorn app.main:app --reload

6. Start the Celery worker:
celery --app app.worker.celery_app worker --beat -s celerybeat-schedule --loglevel INFO

# Usage
Once the application is up and running, you can use the following endpoints:
- GET /: Returns a simple greeting message and the name of the application.

- GET /products: Returns a list of all products in the database.

- POST /events/scrape: Accepts product data in the request body and creates a new product entry in the database.

- GET /products/{asin}: Returns details of a specific product identified by its ASIN.
 
- GET /products/{asin}/events: Returns a list of scrape events associated with a specific product.


# Background Tasks
The application includes a background task implemented with Celery. It periodically scrapes product data from Amazon at a configurable interval. The interval is set to every 5 minutes by default. You can modify the interval by changing the crontab expression in the setup_periodic_tasks function of app.worker module.

# Database
The application uses Cassandra as the database for storing product and scrape event data. The database connection details are read from the environment variables ASTRA_DB_CLIENT_ID and ASTRA_DB_CLIENT_SECRET. Make sure to provide the correct Astra DB client ID and secret in the .env file.

