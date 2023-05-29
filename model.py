from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from pydantic import BaseModel


class MyModel(BaseModel):
    id: int
    value: int


# data = {
#     "asin": "TESTING123D",
#     "title": "Mark 1adsf"
# }


# List View -> Detail View
class Product(Model): # -> table
    __keyspace__ = "scraper_app" #
    asin = columns.Text(primary_key=True, required=True)
    title = columns.Text()
    brand = columns.Text()
    price_str = columns.Text(default="-100")
    country_of_origin = columns.Text()

# Detail View for asin
class ProductScrapeEvent(Model): # -> table
    __keyspace__ = "scraper_app" #
    uuid = columns.UUID(primary_key=True) # uuid.uuid1() -> #time
    asin = columns.Text(index=True)
    title = columns.Text()
    brand = columns.Text()
    country_of_origin = columns.Text() 
    price_str = columns.Text(default="-100")


class Cities(Model): # -> table
    __keyspace__ = "cityinfo" #
    # id = columns.Text(primary_key=True, required=True)
    id = columns.Integer(primary_key=True)
    name = columns.Text()
    country = columns.Text()


    class config:
        orm_mode = True


class States(Model):
    __keyspace__ = "cityinfo"

    # id = columns.Integer(primary_key=True)
    uuid = columns.UUID(primary_key=True)
    name = columns.Text()
    # state = columns.Text()
    

    class config:
        orm_mode = True

