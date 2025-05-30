from jwt import encode, decode
from datetime import datetime, timedelta
from typing import Optional


class JWTManager:
    def __init__(self, secret_key: str = "my_secret_key"):
        self.secret_key = secret_key
        self.algorithm = "HS256"
    
    def create_token(self, data: dict) -> str:
        """Crea un token JWT con los datos proporcionados"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=24)
        to_encode.update({"exp": expire})
        token = encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return token
    
    def validate_token(self, token: str) -> Optional[dict]:
        """Valida un token JWT y retorna los datos si es válido"""
        try:
            decoded_data = decode(token, self.secret_key, algorithms=[self.algorithm])
            return decoded_data if decoded_data["exp"] >= datetime.utcnow().timestamp() else None
        except Exception:
            return None
