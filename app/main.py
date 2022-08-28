from enum import Enum
from typing import Union
from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet",
    resnet = "resnet",
    lenet = "lenet"


app = FastAPI()


@app.get("/")
async def root():
	return {"message": "Hello world"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "DeepLearning FTW!"}
    
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# --------------------------------------------------
fake_items_db = [
	{"item_name": "Foo", "number": 1},
	{"item_name": "Bar", "number": 2},
	{"item_name": "Baz", "number": 3},
	{"item_name": "Foo", "number": 4},
	{"item_name": "Bar", "number": 5},
	{"item_name": "Baz", "number": 6},
	{"item_name": "Foo", "number": 7},
	{"item_name": "Bar", "number": 8},
	{"item_name": "Baz", "number": 9},
	{"item_name": "Foo", "number": 10},
	{"item_name": "Bar", "number": 11},
	{"item_name": "Baz", "number": 12},
	{"item_name": "Foo", "number": 13},
	{"item_name": "Bar", "number": 14},
	{"item_name": "Baz", "number": 15},
	{"item_name": "Foo", "number": 16},
	{"item_name": "Bar", "number": 17},
	{"item_name": "Baz", "number": 18},
	{"item_name": "Foo", "number": 19},
	{"item_name": "Bar", "number": 20},
	{"item_name": "Baz", "number": 21},
	{"item_name": "Foo", "number": 22},
	{"item_name": "Bar", "number": 23},
	{"item_name": "Baz", "number": 24},
]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Union[str, None] = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
			{"description": "This is an amazing item that has a long description"}
		)
    return item

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
