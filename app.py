from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Union
from pydantic import BaseModel
import jwt  # PyJWT library
from datetime import datetime, timedelta

# Inicializa FastAPI
app = FastAPI(debug=True)

origins = [
    "http://localhost:5173",
    "https://deploy-react-front-g4.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Usuarios predefinidos (email: password)
usuarios = {"a@gmail.com": "12345678"}

# Secret Key para firmar tokens
SECRET_KEY = "ODNn6HmZXiH0yS"
ALGORITHM = "HS256"

# Configura OAuth2 para manejar el envío del token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Modelos de datos
class Item(BaseModel):
    item: Union[str, int]

class ReplaceData(BaseModel):
    new_data: List[Union[str, int]]

class UpdateItem(BaseModel):
    index: int
    new_value: Union[str, int]

# Función para generar el token JWT
def generate_token(user: str):
    expiration = datetime.utcnow() + timedelta(hours=2)  # Token expira en 2 horas
    payload = {"sub": user, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Función para validar el token JWT
def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Dependencia para validar el token en cada endpoint protegido
def get_current_user(token: str = Depends(oauth2_scheme)):
    return validate_token(token)

@app.options("/login")
async def options_login():
    return JSONResponse(
        content={"message": "Preflight request successful"},
        headers={
            "Access-Control-Allow-Origin": "https://deploy-reactfront.onrender.com",  # Cambia esto según el origen exacto
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type",
            "Access-Control-Allow-Credentials": "true",
        },
    )
    
# Login (genera un JWT)
@app.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    user = credentials.username
    password = credentials.password

    # Verificar credenciales
    if user not in usuarios or usuarios[user] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generar token
    token = generate_token(user)
    return {"access_token": token, "token_type": "bearer"}

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Union
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

# Inicializa FastAPI
app = FastAPI(debug=True)

# Configurar CORS
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Usuarios predefinidos (email: password)
usuarios = {"a@gmail.com": "12345678"}

# Secret Key para firmar tokens
SECRET_KEY = "ODNn6HmZXiH0yS"
ALGORITHM = "HS256"

# Configura OAuth2 para manejar el envío del token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Datos en memoria
data: List[Union[str, int]] = []

# Modelos de datos
class Item(BaseModel):
    item: Union[str, int]

class ReplaceData(BaseModel):
    new_data: List[Union[str, int]]

class UpdateItem(BaseModel):
    index: int
    new_value: Union[str, int]

# Función para generar el token JWT
def generate_token(user: str):
    expiration = datetime.utcnow() + timedelta(hours=2)
    payload = {"sub": user, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Función para validar el token JWT
def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Dependencia para validar el token
def get_current_user(token: str = Depends(oauth2_scheme)):
    return validate_token(token)

# Login (genera un JWT)
@app.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    user = credentials.username
    password = credentials.password

    if user not in usuarios or usuarios[user] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = generate_token(user)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/refresh")
async def refresh_token(current_user: str = Depends(get_current_user)):
    """
    Valida el token actual y genera un nuevo token si es válido.
    """
    # Generar un nuevo token basado en el usuario actual
    new_token = generate_token(current_user)
    return {"access_token": new_token, "token_type": "bearer"}


# Endpoints protegidos
@app.get("/")
async def get_data(request: Request, current_user: str = Depends(get_current_user)):
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
        "data": data,
        "current_user": current_user,
    }

@app.post("/")
async def add_data(request: Request, item: Item, current_user: str = Depends(get_current_user)):
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    method = request.method
    url = str(request.url)
    cookies = request.cookies
    body = await request.body()

    data.append(item.item)
    return {
        "method": method,
        "url": url,
        "headers": headers,
        "query_params": query_params,
        "cookies": cookies,
        "body": body.decode('utf-8'),
        "data": data,
        "current_user": current_user,
    }

@app.put("/")
async def replace_data(request: Request, new_data: ReplaceData, current_user: str = Depends(get_current_user)):
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
        "data": data,
        "current_user": current_user,
    }

@app.patch("/")
async def update_data(request: Request, update: UpdateItem, current_user: str = Depends(get_current_user)):
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
        "data": data,
        "current_user": current_user,
    }

@app.delete("/")
async def delete_data(request: Request, index: int, current_user: str = Depends(get_current_user)):
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
        "data": data,
        "current_user": current_user,
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
        "message": "OPTIONS request received. You can use GET, POST, PUT, PATCH, DELETE, OPTIONS.",
    }
