from fastapi import FastAPI, Request, HTTPException
from typing import List, Union

app = FastAPI()

# Datos en memoria
data: Union[List[str], List[int]] = []

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
async def add_data(request: Request, item: Union[str, int]):
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    method = request.method
    url = str(request.url)
    cookies = request.cookies
    body = await request.body()
    
    data.append(item)
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
async def replace_data(request: Request, new_data: List[Union[str, int]]):
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    method = request.method
    url = str(request.url)
    cookies = request.cookies
    body = await request.body()
    
    global data
    data = new_data
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
async def update_data(request: Request, index: int, new_value: Union[str, int]):
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    method = request.method
    url = str(request.url)
    cookies = request.cookies
    body = await request.body()
    
    if index < 0 or index >= len(data):
        raise HTTPException(status_code=400, detail="Index out of range")
    data[index] = new_value
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
