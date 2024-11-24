from fastapi import FastAPI, Request, HTTPException
from typing import List, Union
from pydantic import BaseModel

app = FastAPI()

# Datos en memoria
data: Union[List[str], List[int]] = []

# Modelo Pydantic para validación
class Item(BaseModel):
    item: Union[str, int]

class ReplaceData(BaseModel):
    new_data: List[Union[str, int]]

class UpdateItem(BaseModel):
    index: int
    new_value: Union[str, int]

@app.get("/")
async def get_data(request: Request):
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    method = request.method
    url = str(request.url)
    cookies = request.cookies
    body = await request.body()
    
    return {
        "method": method,
        "url": url,
        "headers": headers,
        "query_params": query_params,
        "cookies": cookies,
        "body": body.decode('utf-8'),
        "data": data
    }

@app.post("/")
async def add_data(request: Request, item: Item):
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    method = request.method
    url = str(request.url)
    cookies = request.cookies
    body = await request.body()

    data.append(item.item)  # Solo agrega el valor del campo `item`
    return {
        "method": method,
        "url": url,
        "headers": headers,
        "query_params": query_params,
        "cookies": cookies,
        "body": body.decode('utf-8'),
        "message": "Item added",
        "data": data
    }

@app.put("/")
async def replace_data(request: Request, new_data: ReplaceData):
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    method = request.method
    url = str(request.url)
    cookies = request.cookies
    body = await request.body()
    
    global data
    data = new_data.new_data
    return {
        "method": method,
        "url": url,
        "headers": headers,
        "query_params": query_params,
        "cookies": cookies,
        "body": body.decode('utf-8'),
        "message": "Data replaced",
        "data": data
    }

@app.patch("/")
async def update_data(request: Request, update: UpdateItem):
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    method = request.method
    url = str(request.url)
    cookies = request.cookies
    body = await request.body()
    
    if update.index < 0 or update.index >= len(data):
        raise HTTPException(status_code=400, detail="Index out of range")
    data[update.index] = update.new_value
    return {
        "method": method,
        "url": url,
        "headers": headers,
        "query_params": query_params,
        "cookies": cookies,
        "body": body.decode('utf-8'),
        "message": "Item updated",
        "data": data
    }

@app.delete("/")
async def delete_data(request: Request, index: int):
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    method = request.method
    url = str(request.url)
    cookies = request.cookies
    body = await request.body()
    
    if index < 0 or index >= len(data):
        raise HTTPException(status_code=400, detail="Index out of range")
    removed_item = data.pop(index)
    return {
        "method": method,
        "url": url,
        "headers": headers,
        "query_params": query_params,
        "cookies": cookies,
        "body": body.decode('utf-8'),
        "message": "Item deleted",
        "removed_item": removed_item,
        "data": data
    }
