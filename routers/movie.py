from typing import List
from fastapi import APIRouter

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from config.database import Session
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    db = Session()
    movies = MovieService(db).get_movies()
    return JSONResponse(jsonable_encoder(movies), status_code=200)

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int) -> Movie:
    db = Session()
    movie = MovieService(db).get_movie(id)
    return JSONResponse(jsonable_encoder(movie), status_code=200) if movie else JSONResponse(content={"message": "Movie not found"}, status_code=404)

@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str) -> List[Movie]:
    db = Session()
    movies = MovieService(db).get_movies_by_category(category)
    return JSONResponse(jsonable_encoder(movies), status_code=200)

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(content={"message": "Movie created"}, status_code=201)