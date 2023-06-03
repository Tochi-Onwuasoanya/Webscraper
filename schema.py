from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

data = {
    "asin": "TESTING123D",
    "title": "Mark 1adsf"
}

class Product(Model):
    """
    Represents a product in the 'scraper_app' keyspace.
    """

    __keyspace__ = "scraper_app"
    asin = columns.Text(primary_key=True, required=True)
    title = columns.Text()
    brand = columns.Text()
    price_str = columns.Text(default="-100")
    country_of_origin = columns.Text()

class ProductScrapeEvent(Model):
    """
    Represents a scrape event for a product in the 'scraper_app' keyspace.
    """

    __keyspace__ = "scraper_app"
    uuid = columns.UUID(primary_key=True)
    asin = columns.Text(index=True)
    title = columns.Text()
    brand = columns.Text()
    country_of_origin = columns.Text()
    price_str = columns.Text(default="-100")
