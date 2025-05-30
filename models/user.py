from config.database import Base
from sqlalchemy import Column, Integer, String
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    def verify_password(self, password: str) -> bool:
        """Verifica si la contraseña proporcionada es correcta"""
        return pwd_context.verify(password, self.hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Genera el hash de una contraseña"""
        return pwd_context.hash(password)
