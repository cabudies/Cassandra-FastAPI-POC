from typing import Union

from cassandra.cluster import Cluster
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse, JSONResponse

from model import MyModel


USERPROFILE_DOC_TYPE = "userprofile"


# def get_bucket():
#     cluster = Cluster(
#         "couchbase://couchbasehost:8091?fetch_mutation_tokens=1&operation_timeout=30&n1ql_timeout=300"
#     )
#     authenticator = PasswordAuthenticator("username", "password")
#     cluster.authenticate(authenticator)
#     bucket: Bucket = cluster.open_bucket("bucket_name", lockmode=LOCKMODE_WAIT)
#     bucket.timeout = 30
#     bucket.n1ql_timeout = 300
#     return bucket

# cluster = Cluster(['172.17.0.2'])
# cluster = Cluster(['0.0.0.0'], port=9042)
cluster = Cluster(['127.0.0.1'], port=9042)
# cluster = Cluster(['cas1'], port=9042)
# cluster = Cluster(['106.196.27.89'])
# cluster = Cluster()
session = cluster.connect('cityinfo')
session.execute('USE cityinfo')
rows = session.execute('SELECT * FROM cities')
for row in rows:
    print(row.id, "-", row.name, "-", row.country)



class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    type: str = USERPROFILE_DOC_TYPE
    hashed_password: str


# def get_user(bucket: Bucket, username: str):
#     doc_id = f"userprofile::{username}"
#     result = bucket.get(doc_id, quiet=True)
#     if not result.value:
#         return None
#     user = UserInDB(**result.value)
#     return user


# FastAPI specific code
app = FastAPI()


# @app.get("/users/{username}", response_model=User)
# def read_user(username: str):
#     bucket = get_bucket()
#     user = get_user(bucket=bucket, username=username)
#     return user

@app.get("/models/{table}")
async def get_models(table: str):
    """
    Return all models
    """
    rows = session.execute("SELECT * FROM {};".format(table))
    data = {'items': {}}
    for row in rows:
        data['items'][row.id] = row.value
    data['count'] = len(data['items'])
    return JSONResponse(
        data,
        status_code=200
    )


@app.post("/model/{table}")
async def post_model(table: str, item: MyModel):
    """
    Add a new model in the table
    """
    returned_value = session.execute(
        "INSERT INTO {} (id, value) VALUES ({}, {});".format(table, item.id, item.value)
    )
    return JSONResponse(
        {'detail': "model has been added"},
        status_code=200
    )


