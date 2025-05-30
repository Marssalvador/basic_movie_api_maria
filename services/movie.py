from models.movie import Movie as MovieModel
from schemas.movie import Movie

class MovieService():
    def __init__(self, repository) -> None:
        self.db = repository

    def get_movies(self):
        movies = self.db.query(MovieModel).all()
        return movies

    def get_movie(self, id: int):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return movie

    def get_movies_by_category(self, category: str):
        movies = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return movies

    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()
        return
