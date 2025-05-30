from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from routers.movie import movie_router

app = FastAPI()
app.title = "My movie API"
app.version = "0.0.1"


app.include_router(movie_router)


@app.get('/', tags=['home'])
def message():
    return HTMLResponse(content="<h1>Hello World!!</h1>", status_code=200)