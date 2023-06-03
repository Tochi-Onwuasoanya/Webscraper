from celery import Celery
from celery.schedules import crontab
from celery.signals import beat_init, worker_process_init
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table

from . import config, crud, db, models, schema, scraper

# Create a Celery app
celery_app = Celery(__name__)

# Get settings from configuration
settings = config.get_settings()

# Set up Redis URL for broker and result backend
REDIS_URL = settings.redis_url
celery_app.conf.broker_url = REDIS_URL
celery_app.conf.result_backend = REDIS_URL

# Assign models to variables for easier access
Product = models.Product
ProductScrapeEvent = models.ProductScrapeEvent

# Celery task to be executed on startup
def celery_on_startup(*args, **kwargs):
    # Shut down existing Cassandra connections
    if connection.cluster is not None:
        connection.cluster.shutdown()
    if connection.session is not None:
        connection.session.shutdown()
    
    # Establish new Cassandra connection
    cluster = db.get_cluster()
    session = cluster.connect()
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    
    # Sync Cassandra tables
    sync_table(Product)
    sync_table(ProductScrapeEvent)

# Connect the celery_on_startup function to Celery signals
beat_init.connect(celery_on_startup)
worker_process_init.connect(celery_on_startup)

# Define periodic tasks
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, *args, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*/5"),
        scrape_products.s()
    )

# Celery task to perform a random task
@celery_app.task
def random_task(name):
    print(f"Who throws a shoe. Honestly, {name}.")

# Celery task to list products
@celery_app.task
def list_products():
    q = Product.objects().all().values_list("asin", flat=True)
    print(list(q))

# Celery task to scrape a specific ASIN
@celery_app.task
def scrape_asin(asin):
    s = scraper.Scraper(asin=asin, endless_scroll=True)
    dataset = s.scrape()
    try:
        validated_data = schema.ProductListSchema(**dataset)
    except:
        validated_data = None
    if validated_data is not None:
        product, _ = crud.add_scrape_event(validated_data.dict())
        return asin, True
    return asin, False

# Celery task to scrape all products
@celery_app.task
def scrape_products():
    print("Doing scraping")
    q = Product.objects().all().values_list("asin", flat=True)
    for asin in q:
        scrape_asin.delay(asin)
