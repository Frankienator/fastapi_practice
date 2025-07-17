from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()


@app.get("/items/")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results["q"] = q
    return results

# We already learned simple validation within Query parameters and request bodies such as "Required".
# Let's check out some further validation so that for example a query, whenever it is provided, does not exceed 50 characters.

@app.get("/items/validated/")
async def read_items_validated(q: Annotated[str | None, Query(max_length=50)] = None):
# async def read_items_validated(q: str | None = Query(default=None, max_length=50)): # Old version, take care since it is not allowed to set the default both inside and outside of Query()
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results["q"] = q
    return results

# Annotated is used in the type for the q parameter instead.
# By doing this, we can add metadata to the value, as done in the provided function.
# By adding Query() to the metadata, we are able to further granulate the validation.

# There are many validation concepts which can be added using query, such as min_length or pattern (for RegEx)

@app.get("/items/validated/")
async def read_items_validated(q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")] = None):
    pass


# Similar to query parameters, we can use default values by defining them in the function head.
# They do not necessarily need to be None as provided before.

# To make a value Required, we can not place a default value.
# So the following would be required:
@app.get("/items/validated/")
async def read_items_validated(q: Annotated[str, Query(min_length=3, max_length=50, pattern="^fixedquery$")]):
    pass


# But if we want the value to be required, with the option that it is none (e.g. if we want to force that something is sent even if None or Null), we use the following construct:
@app.get("/items/validated/")
async def read_items_validated(q: Annotated[str | None, Query(min_length=3)]):
    pass

# To properly ask for multiple values in the form of a list for example, we can just set the type accordingly:

@app.get("/items/validated/")
async def read_items_validated(q: Annotated[list[str], Query(min_length=3, max_length=50, pattern="^fixedquery$")] = ["foo", "bar"]):
    pass

# This for example would make it possible, to pass the same query parameter multiple times and it is read as a list, so in that case:
# http://localhost:8000/items/validated/?q=foo&q=bar

# As we can see above, we can also use a list as default value.

# There is lots more of metadata to set such as "title" or "description":

@app.get("/items/metadata/")
async def read_items_metadata (
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query",
            min_length=3
        )
    ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results["q"] = q
    return results

# Another interesting concept is the setting of aliases for a query parameter:
@app.get("/items/validated/")
async def read_items_validated(q: Annotated[list[str], Query(alias="item-query")] = None):
    pass

# By doing this, you do not necessarily have to use q=... but can also use the alias item-query=...

# Another one is deprecated, which can let users know within the docs, whether a parameter is deprecated.
# Similarly, using include_in_schema=False within query, we can hide a parameter from the automatic documentation.
# This is especially interesting when we want to implement internal parameters

# Custom validation with pydantic

# We can utilize Pydantic's AfterValidator (similarly BeforeValidator) to create a custom validation.
# This is done the following way:

from pydantic import AfterValidator

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

# We set up our custom validation within a function
def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError("Invalid ID format, must start with 'isbn-' or 'imdb-'")
    return id

@app.get("/items/")
async def read_items(
    id: Annotated[str | None, Query(AfterValidator(check_valid_id))] = None
):
    pass

# The AfterValidator is set within Query() and takes our custom validation function as parameter.
# It then applies the validation onto our input "id".


