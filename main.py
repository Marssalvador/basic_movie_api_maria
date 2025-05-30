from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from routers.movie import movie_router
from routers.user import user_router
from middlewares.error_handler import ErrorHandler

app = FastAPI()
app.title = "My movie API"
app.version = "1.0.0"

# Agregar middleware de manejo de errores
app.add_middleware(ErrorHandler)

# Incluir routers
app.include_router(movie_router)
app.include_router(user_router)


@app.get('/', tags=['home'])
def message():
    return HTMLResponse(content="<h1>Movie API with Authentication</h1><p>API funcionando correctamente!</p>", status_code=200)