from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items")
def read_item(item_id: int, q: Union[str, None] = None):
    print(item_id, 'was queried')
    return {"item_id": item_id, "q": q}