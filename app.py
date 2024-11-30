from fastapi import FastAPI, Request, Response, HTTPException
from typing import List, Union
from pydantic import BaseModel
from utils import *
from control_usuario import *
from token_processing import *
from flask_exceptions import *

app = FastAPI(debug=True)

# Datos en memoria
data: Union[List[str], List[int]] = []

usuarios : dict[str,str] = {"juan" : "1234"}

# Modelo Pydantic para validación
class Item(BaseModel):
    item: Union[str, int]

class ReplaceData(BaseModel):
    new_data: List[Union[str, int]]

class UpdateItem(BaseModel):
    index: int
    new_value: Union[str, int]


@app.post("/login")
async def login(request: Request,response : Response):
    try:
        body = await request.json()
        user,password = procesar_body_usuario_contraseña(body)

        if not user or not password:
            raise UserPasswordNotFoundException("")

        if not user_password_correcto(usuarios, user, password):
            raise InvalidCredentialsException("")

        # Generar tokens
        key, token = generate_token(user, password)

        # Configurar cookies seguras
        response.set_cookie(
            key="jwk_token",
            value=key,
            httponly=True,
            secure=True,  
            samesite="Strict"
        )

        response.set_cookie(
            key="jwt_token",
            value=token,
            httponly=True,  
            secure=True,  
            samesite="Strict"
        )

        return {"message": "Inicio de sesión exitoso.",
                "cookies" : request.cookies}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="El cuerpo debe estar en formato JSON.")
    except UserPasswordNotFoundException:
        
        raise HTTPException(status_code=400, detail="Usuario o contraseña faltantes.")
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas.")


@app.get("/")
async def get_data(request: Request):
    try:
       headers = dict(request.headers)
       query_params = dict(request.query_params)
       method = request.method
       url = str(request.url)
       cookies = request.cookies
       body = await request.body()

       if(comprobar_cookies(usuarios,cookies) == False):
        raise InvalidCredentialsException("")
    
       return {
        "method": method,
        "url": url,
        "headers": headers,
        "query_params": query_params,
        "cookies": cookies,
        "body": body.decode('utf-8'),
        "data": data
       }
    
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas.")

@app.post("/")
async def add_data(request: Request, item: Item):

    try:
       headers = dict(request.headers)
       query_params = dict(request.query_params)
       method = request.method
       url = str(request.url)
       cookies = request.cookies
       body = await request.body()

       if(comprobar_cookies(usuarios,cookies) == False):
        raise InvalidCredentialsException("")
       
       data.append(item.item)
       return {
        "method": method,
        "url": url,
        "headers": headers,
        "query_params": query_params,
        "cookies": cookies,
        "body": body.decode('utf-8'),
        "data": data
       }
    
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas.")

@app.put("/")
async def replace_data(request: Request, new_data: ReplaceData):

    try:
       headers = dict(request.headers)
       query_params = dict(request.query_params)
       method = request.method
       url = str(request.url)
       cookies = request.cookies
       body = await request.body()

       if(comprobar_cookies(usuarios,cookies) == False):
        raise InvalidCredentialsException("")
       
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
    
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas.")

@app.patch("/")
async def update_data(request: Request, update: UpdateItem):

    try:
       headers = dict(request.headers)
       query_params = dict(request.query_params)
       method = request.method
       url = str(request.url)
       cookies = request.cookies
       body = await request.body()

       if(comprobar_cookies(usuarios,cookies) == False):
        raise InvalidCredentialsException("")
    
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
    
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas.")

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

@app.options("/")
async def options_data(request: Request):
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
        "message": "OPTIONS request received. You can use GET, POST, PUT, PATCH, DELETE, OPTIONS."
    }

