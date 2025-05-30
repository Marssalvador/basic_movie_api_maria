from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user import User
from schemas.user import UserCreate, UserLogin
from utils.jwt_manager import JWTManager
from typing import Optional


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.jwt_manager = JWTManager()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por su email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Obtiene un usuario por su nombre de usuario"""
        return self.db.query(User).filter(User.username == username).first()
    
    def create_user(self, user: UserCreate) -> User:
        """Crea un nuevo usuario"""
        # Verificar si el email ya existe
        if self.get_user_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Verificar si el username ya existe
        if self.get_user_by_username(user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Crear el usuario
        hashed_password = User.get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def authenticate_user(self, user_login: UserLogin) -> Optional[str]:
        """Autentica un usuario y retorna un token JWT"""
        user = self.get_user_by_email(user_login.email)
        if not user or not user.verify_password(user_login.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        token_data = {"sub": user.email, "user_id": user.id}
        access_token = self.jwt_manager.create_token(token_data)
        return access_token
