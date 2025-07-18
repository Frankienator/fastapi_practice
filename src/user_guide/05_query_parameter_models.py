from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(
    filter_query: Annotated[FilterParams, Query()]
):
    return filter_query

# FastAPI fetches the pydantic model and extracts each field to return the pydantic model you defined.

# For our example, the following would be a valid query model:

# {
#   "limit": 12,
#   "offset": 3,
#   "order_by": "updated_at",
#   "tags": [
#     "a",
#     "string"
#   ]
# }

# since we use a query model, the actual request looks as follows: http://localhost:8000/items/?limit=12&offset=3&order_by=updated_at&tags=a&tags=string

# This gives us a similar functionality to request bodies by using query parameters, although it is not recommended to use them as such.


# Forbidding extra query parameters
# there may be some cases, where you want to restrict query parameters.
# This is done the following way:

class FilterParamsNoExtras(BaseModel):
    model_config = {"extra": "forbid"} # we set the model config to "extra":"forbid"

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/noExtras")
async def find_items_noExtras(
    filter_query: Annotated[FilterParamsNoExtras, Query()]
):
    return filter_query

# while our previous call:
# http://localhost:8000/items/?limit=12&offset=3&order_by=updated_at&tags=a&tags=string
# would work, adding any extra query parameter in wouldn't work unless explicitly set (but then the model has to be defined explicitly which is bad)