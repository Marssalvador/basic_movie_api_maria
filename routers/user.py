from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from config.database import Session as SessionLocal
from services.user import UserService
from schemas.user import UserCreate, UserLogin, UserResponse, Token


user_router = APIRouter()


def get_db():
    """Dependency para obtener la sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.post('/auth/register', tags=['auth'], response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario en el sistema"""
    try:
        user_service = UserService(db)
        new_user = user_service.create_user(user)
        return JSONResponse(
            content=jsonable_encoder(new_user), 
            status_code=201
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )


@user_router.post('/auth/login', tags=['auth'], response_model=Token, status_code=200)
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Autentica un usuario y devuelve un token JWT"""
    try:
        user_service = UserService(db)
        access_token = user_service.authenticate_user(user_credentials)
        return JSONResponse(
            content={
                "access_token": access_token,
                "token_type": "bearer"
            },
            status_code=200
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during authentication"
        )
