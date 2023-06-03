# Endpoint to Ingest Data for FastAPI & AstraDB

from typing import List
from fastapi import FastAPI
from cassandra.cqlengine.management import sync_table
from . import db, config, crud, models, schema

settings = config.get_settings()
Product = models.Product
ProductScrapeEvent = models.ProductScrapeEvent

app = FastAPI()

session = None

@app.on_event("startup")
def on_startup():
    """
    Function executed on application startup.
    It establishes a session with the Cassandra cluster and syncs the Product and ProductScrapeEvent tables.
    """
    global session
    session = db.get_session()
    sync_table(Product)
    sync_table(ProductScrapeEvent)

@app.get("/")
def read_index():
    """
    Endpoint to return a simple hello world message along with the configured name.
    """
    return {"hello": "world", "name": settings.name}

@app.get("/products", response_model=List[schema.ProductListSchema])
def products_list_view():
    """
    Endpoint to retrieve a list of all products.
    """
    return list(Product.objects.all())

@app.post("/events/scrape")
def events_scrape_create_view(data: schema.ProductListSchema):
    """
    Endpoint to create a scrape event for a product.
    It calls the 'add_scrape_event' function from the 'crud' module and returns the created product.
    """
    product, _ = crud.add_scrape_event(data.dict())
    return product

@app.get("/products/{asin}")
def products_detail_view(asin):
    """
    Endpoint to retrieve detailed information about a product.
    It fetches the product information from the Product table and retrieves the recent scrape events for the product.
    Returns the product data along with the associated scrape events.
    """
    data = dict(Product.objects.get(asin=asin))
    events = list(ProductScrapeEvent.objects().filter(asin=asin).limit(5))
    events = [schema.ProductScrapeEventDetailSchema(**x) for x in events]
    data['events'] = events
    data['events_url'] = f"/products/{asin}/events"
    return data

@app.get("/products/{asin}/events", response_model=List[schema.ProductScrapeEventDetailSchema])
def products_scrapes_list_view(asin):
    """
    Endpoint to retrieve a list of scrape events for a product.
    """
    return list(ProductScrapeEvent.objects().filter(asin=asin))
