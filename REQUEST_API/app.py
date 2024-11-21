from fastapi import FastAPI,  Request

app = FastAPI()

@app.get("/")
async def handle_get(request: Request):
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
        "body": body.decode('utf-8')
    }

@app.post("/")
async def handle_post(request: Request):
    headers = dict(request.headers)
    method = request.method
    url = str(request.url)
    body = await request.body()
    
    return {
        "method": method,
        "url": url,
        "headers": headers,
        "body": body.decode('utf-8')
    }