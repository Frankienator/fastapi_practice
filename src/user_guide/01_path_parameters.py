from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# We define a path parameter within the path with curly braces, and use the same name in the function header
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return{"item_id": item_id}

# this will be called, as the function is defined before the /users/{user_id} path function
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# this will never be called as the previous /users/{user_id} function covers this path
@app.get("/users/you")
async def read_user_you():
    return {"user_id": "not the current user"}

#similar here:
@app.get("/users")
async def get_users():
    return ['Elmo', 'Bert']

@app.get("/users")
async def get_users_too():
    return ['Spongebob', 'Patrick']
# In this case, Elmo and Bert will always be returned.


# Predefined Values

from enum import Enum

class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'

# app = FastAPI() => Defined above

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name is ModelName.lenet:
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}

# We can use Enums combined with typechecking to fix what we want to get in our path
# With the help of type checking, our path parameter is an Enumeration parameter.
# Hence, only the values defined in the Enum (ModelName) are valid and the rest results in an error


#Path convertor

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path", file_path}