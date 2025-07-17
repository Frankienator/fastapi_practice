from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/")
async def root():
    return {"Message:", "Hello World"}


# Query Parameters

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return {
        "Query_Params" : f"Skip: {skip}, Limit: {limit}",
        "Content" : fake_items_db[skip : skip + limit]    
            }

# An example query would be http://localhost:8000/items?skip=2&limit=8
# Utilizing the defaults that we set within the python function the following two are equal:
# http://localhost:8000/items?skip=0&limit=10
# http://localhost:8000/items

# you can also only set one of the params. The other one would be the default so:
# http://localhost:8000/items?skip=5 is equal to
# http://localhost:8000/items?skip=5&limit=10


# Optional Parameters

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# By defaulting a variable to None as shown, we define optional parameters


# Query parameter type conversion:

@app.get("/items/typeconv/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# We can use the following values for short due to type conversion:
# ... &short=1
# ... &short=True
# ... &short=true
# ... &short=on
# ... &short=yes
# or any other case variation


# Multiple path and query parameters
# The order doesn't matter, as the detection is done by name:

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "user_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is not the greatest description, this is a tribute"})
    return item

# e.g.: http://localhost:8000/users/5/items/abba?q=this+is+a+query


# Required Query Parameters

# As mentioned before, when no default is set, the query parameter is required.
# So for example, the following wouldn't work without setting the query parameter:

@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

# without setting the needy query parameter, an error is returned