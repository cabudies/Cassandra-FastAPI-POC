from typing import Union
import uuid
from cassandra.cluster import Cluster
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse, JSONResponse
from cassandra.cqlengine.management import sync_table

# from model import MyModel
# from . import db, model
import db, model, dto


USERPROFILE_DOC_TYPE = "userprofile"


### base code
# cluster = Cluster(['127.0.0.1'], port=9042)
# session = cluster.connect('cityinfo')
# session.execute('USE cityinfo')
# rows = session.execute('SELECT * FROM cities')
# for row in rows:
#     print(row.id, "-", row.name, "-", row.country)


# Product = models.Product
# ProductScrapeEvent = models.ProductScrapeEvent
Cities = model.Cities
state_table = model.States


app = FastAPI()

session = None

@app.on_event("startup")
def on_startup():
    global session
    session = db.get_session()
    # sync_table(Product)
    # sync_table(ProductScrapeEvent)
    sync_table(Cities)
    sync_table(state_table)



@app.get("/states")
def states_list_view(
    # search_criteria: dto.StatesSearchSchema
):
    query = state_table

    # name = None
    name = "Punjab"

    if name:
        # query = query.objects.filter(state_table.name == name)
        query = query.objects.filter(name = name)
        result = query.get()
    else:
        query = query.objects
        result = query.all()

    return list(result)


@app.post("/states")
def states_create_view(data: dto.StatesSchema):
    new_uuid = uuid.uuid1()
    state = state_table.create(uuid=new_uuid, name=data.name)
    state.save()
    return state


@app.get("/cities")
def cities_list_view():
    return list(Cities.objects.all())
    # return Cities.objects.all()


@app.post("/cities")
def cities_create_view(data: dto.CitiesSchema):
    # city = Cities.create(**data)
    # city = Cities.create(data)
    # data_dict = data.__dict__
    # city = Cities.create(data_dict)
    city = Cities.create(id=5, name=data.name, country=data.country)
    city.save()
    return city
