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
        return new_movie

    def update_movie(self, id: int, movie: Movie):
        """Actualiza una película existente"""
        db_movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        if db_movie:
            update_data = movie.model_dump()
            for field, value in update_data.items():
                setattr(db_movie, field, value)
            self.db.commit()
            return db_movie
        return None

    def delete_movie(self, id: int):
        """Elimina una película por su ID"""
        db_movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        if db_movie:
            self.db.delete(db_movie)
            self.db.commit()
            return True
        return False
