from typing import Optional
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from pydantic import BaseModel
from bson import ObjectId
import uuid
from datetime import datetime


# class PyUUId(ObjectId):
# # class PyUUId(uuid):

#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid objectid")
#         return ObjectId(v)

#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type="string")


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


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
    # uuid: Optional[str] = columns.UUID(primary_key=True, default_factory=PyUUId)
    # uuid: Optional[str] = columns.UUID(primary_key=True, default=uuid.uuid4())
    # uuid: Optional[str] = columns.UUID(primary_key=True, default=uuid.uuid1())
    uuid: Optional[str] = columns.UUID(primary_key=True)
    name = columns.Text()

    # capital = columns.Text(primary_key=True)
    

    class config:
        orm_mode = True

