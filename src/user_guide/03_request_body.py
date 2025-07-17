from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"Message": "Hello World!"}


# To utilize request bodies, you require pydantic models.
# For this, you first need to import BaseModel from pydantic:

from pydantic import BaseModel

# after that, you can create a Data Model based off of BaseModel as a class:

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# with this definition, you can use your data model as request body within your requests:

@app.post("/items/")
async def create_item(item: Item):
    return item

# this model can be more or less considered as a json, or a python dictionary in terms of understanding.
# It may look like:
# {
#     "name": "Foo",
#     "description": "An optional description",
#     "price": 45.2,
#     "tax": 3.5
# }

# As you can see, it is defined as a regular parameter within our function header.

# The optional rows do not have to exist, so the following would be valid too:
# {
#     "name": "Foo",
#     "price": 45.2
# }

# pydantic also supports with type hints and error checks within an editor such as VSCode or PyCharm.

# Of course, it is also possible to access the provided Item Model and execute operations

@app.post("/items/update")
async def create_item_with_tax(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        with_tax = item.price + item.tax
        item_dict['price_with_tax'] = with_tax
    return item_dict


# Request body + path + query parameters

# It is possible to combine Request body, path and query parameters freely (unless you're doing a get where the Request body is prohibited ;) )
# A perfect example where this could happen is a put request or update

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result["q"] = q
    return result