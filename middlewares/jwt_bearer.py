from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from utils.jwt_manager import JWTManager


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.jwt_manager = JWTManager()

    async def __call__(self, request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code."
            )

    def verify_jwt(self, token: str) -> bool:
        """Verifica si el token JWT es válido"""
        payload = self.jwt_manager.validate_token(token)
        return payload is not None
