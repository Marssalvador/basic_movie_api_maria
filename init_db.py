from config.database import engine, Base
from models.movie import Movie
from models.user import User

# Crear todas las tablas
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")