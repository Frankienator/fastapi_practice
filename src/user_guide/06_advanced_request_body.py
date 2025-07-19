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


# Body - Fields

from pydantic import Field


class AnotherItem(BaseModel):
    name: str
    description: str | None = Field(default=None, title="The description of the item", max_length=300)
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.put("/anotherItems/{item_id}")
async def update_anotherItem(
    item_id: int,
    anotherItem: Annotated[AnotherItem, Body(embed=True)]
):
    results = {"item_id": item_id, "anotherItem": anotherItem}
    return results

# The Field() parameter of pydantic makes it possible for us to add metadata, defaults and pydantic-validation to our Item Model.
# This is useful since we can handle responses accordingly then, and proper input validation within our Request Body
# In general, Field() works just like Query(), Path() and Body().


# Body - Nested Models

# utilizing pydantic, you can define, validate, document and use arbitrarily deeply nested Models:

class NestedItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []

@app.put("/nestedItems/{item_id}")
async def update_item(item_id: int, nestedItem: NestedItem):
    pass

# this example contains a python list, but the elements itself are not type secure.
# to change this, we must define our list as such:

from typing import Union

class ListItem(BaseModel):
    name: str
    description: Union[str, None] = None # this Union notation is a different (better readable) way to implement "str | None" for example
    price: float
    tax: Union[float, None] = None
    tags: list[str] = []

# in this example, our tags list is specifically typed to only accept strings.
# For this we also had to import the List parameter from typing.
# Another relevant alternative for List is "set", which doesn't have duplicates and is defined the same as our List:
tags: set[str] = []


# Nested Models

# in pydantic, nothing is stopping us from nesting models.
# Thinking object oriented, this is very good for us.
# An example for this would be:

class InnerItem(BaseModel):
    url: str
    name: str

class OuterItem(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: set[str] = set()
    image: Union[InnerItem, None] = None

# in our OuterItem class, we used an InnerItem typed attribute image.
# This nesting has no limits, and can be applied freely.
# An example of the defined body of type OuterItem would look the following way:

# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2,
#     "tags": ["rock", "metal", "bar"],
#     "image": {
#         "url": "http://example.com/baz.jpg",
#         "name": "The Foo live"
#     }
# }


# Special Types

# Pydantic provides special types which can be used for validation.
# Those types usually inherit from str, and provide special functionality.
# An example would be HttpUrl, which validates the input for a http url string


# Attributes with lists of submodels

# Combining the logic of nested models, and list logic, we can also provide lists or sets of submodels.
# For example:

class OuterItemWithList(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: set[str] = set()
    image: list[InnerItem] = []

# An example for a valid form of this response body model:

# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2,
#     "tags": [
#         "rock",
#         "metal",
#         "bar"
#     ],
#     "images": [
#         {
#             "url": "http://example.com/baz.jpg",
#             "name": "The Foo live"
#         },
#         {
#             "url": "http://example.com/dave.jpg",
#             "name": "The Baz"
#         }
#     ]
# }


# Bodies of pure lists

# If the top level value of the JSON body you expect is a JSON array (= python list), you can declare the type in the function as follows:
@app.post("/images/multiple/")
async def create_multiple_images(images: list[InnerItem]):
    return images


# Similarly, you can declare a body as a dict with keys of some type and values of some other type
# This way, you don't have to know beforehand, what valid field/attribute names are (in contrast to pydantic)
# this is useful if you want to get keys you don't already know about.
# for example:

@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights