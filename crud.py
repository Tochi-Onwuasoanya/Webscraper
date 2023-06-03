# FastAPI, Cassandra & Pydantic

import copy
import uuid
from .models import Product, ProductScrapeEvent

def create_entry(data: dict):
    """
    Creates a new entry in the Product table using the provided data.

    Args:
        data (dict): Data for creating the entry.

    Returns:
        Product: The created Product object.
    """
    return Product.create(**data)


def create_scrape_entry(data: dict):
    """
    Creates a new entry in the ProductScrapeEvent table using the provided data.

    Args:
        data (dict): Data for creating the entry.

    Returns:
        ProductScrapeEvent: The created ProductScrapeEvent object.
    """
    data['uuid'] = uuid.uuid1()  # includes a timestamp
    return ProductScrapeEvent.create(**data)


def add_scrape_event(data: dict, fresh=False):
    """
    Adds a new scrape event to the Product and ProductScrapeEvent tables.

    Args:
        data (dict): Data for creating the scrape event.
        fresh (bool): Flag indicating whether to create a fresh copy of the data.

    Returns:
        Tuple[Product, ProductScrapeEvent]: The created Product and ProductScrapeEvent objects.
    """
    if fresh:
        data = copy.deepcopy(data)
    product = create_entry(data)
    scrape_obj = create_scrape_entry(data)
    return product, scrape_obj
