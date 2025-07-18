from typing import Annotated

from fastapi import FastAPI, Path, Body
from pydantic import BaseModel

app = FastAPI()

# Of course it is possible without issue to mix Path, Query and request body parameter declarations
# Similarly to the rest, you can also set body parameters as optional using None

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None
):
    results = {"item_id": item_id}
    if q:
        results["q"] = q
    if item:
        results["item"] = item
    return results

# In this request, a single request body Item is expected, but FastAPI is also able to handle multiple Request Body parameters, e.g. Item and User:

class User(BaseModel):
    username: str
    full_name: str | None = None

@app.put("/items/{item_id}")
async def update_item_user(
    item_id: int,
    user: User,
    item: Item
):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

# in that case, pydantic recognizes multiple models, and puts them into a single big body.
# so 
# 
#   "item": {
#       "name": "Foo",
#       "description": "The pretender",
#       "price": 42.0,
#       "tax": 3.2
#   }

#   "user": {
#       "username": "dave",
#       "full_name": "Dave Grohl"
#   }
# 

# turns into:

# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     }
# }


# Singular values in body

# When having multiple bodies as before, we can utilize Annotated[type, Body] as typing to tell FastAPI that a parameter is part of a body.
# so for example if we want to add importance to our previous body, we define the function header as such:

@app.put("/items/{item_id}")
async def update_item_user(
    item_id: int,
    user: User,
    item: Item,
    importance: Annotated[int, Body()]
):
    pass

# this would add the importance variable onto the same layer as our user and item Model Objects.
# This does not hinder adding query parameters, which can still be added as learned.

# Embedding a single body parameter
# If we only have a single request body Model, but want to embed it a layer deeper, so not {key1: val1, key2: val2, ...} but {item: {key1: val1, ...}},
# we can use "Body(embed=True)" as such:

@app.post("/items/")
async def create_item(
    item: Annotated[Item, Body(embed=True)]
):
    results = {"item": item}
    return results

