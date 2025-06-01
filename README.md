# Movie API con Autenticación JWT

Una API REST completa para gestión de películas con sistema de autenticación JWT, desarrollada con FastAPI y SQLAlchemy.

## Características

- **Autenticación JWT**: Sistema completo de registro e inicio de sesión
- **CRUD de Películas**: Crear, leer, actualizar y eliminar películas
- **Protección de Endpoints**: Rutas protegidas que requieren autenticación
- **Manejo de Errores**: Middleware centralizado para gestión de errores
- **Documentación Automática**: Swagger UI y ReDoc integrados
- **Base de Datos**: SQLite con SQLAlchemy ORM
- **Validación de Datos**: Schemas con Pydantic
- **Arquitectura Modular**: Código organizado y escalable

## Estructura del Proyecto

```
 basic_movie_api_maria/
├── config/              # Configuración de base de datos
│   ├── __init__.py
│   └── database.py         # Configuración SQLAlchemy
├── middlewares/         # Middleware personalizados
│   ├── __init__.py
│   ├── error_handler.py    # Manejo centralizado de errores
│   └── jwt_bearer.py       # Validación de tokens JWT
├── models/              # Modelos de base de datos
│   ├── __init__.py
│   ├── movie.py           # Modelo de película
│   └── user.py            # Modelo de usuario
├── routers/             # Rutas de la API
│   ├── __init__.py
│   ├── movie.py           # Endpoints de películas
│   └── user.py            # Endpoints de autenticación
├── schemas/             # Esquemas de validación
│   ├── __init__.py
│   ├── movie.py           # Schemas de película
│   └── user.py            # Schemas de usuario
├── services/            # Lógica de negocio
│   ├── __init__.py
│   ├── movie.py           # Servicios de películas
│   └── user.py            # Servicios de usuarios
├── utils/               # Utilidades
│   ├── __init__.py
│   └── jwt_manager.py     # Gestión de tokens JWT
├── main.py             # Archivo principal de la aplicación
├── init_db.py          # Inicializador de base de datos
├── database.sqlite     # Base de datos SQLite
├── requirements.txt    # Dependencias del proyecto
└── README.md          # Este archivo
```

## 🛠 Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd basic_movie_api_maria
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Inicializar la base de datos
```bash
python init_db.py
```

### 4. Ejecutar la aplicación
```bash
# Puerto por defecto (8000)
uvicorn main:app --reload

# Puerto personalizado (ejemplo: 8001)
uvicorn main:app --reload --port 8001
```

## Documentación de la API

Una vez que la aplicación esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **API Principal**: http://localhost:8001

## Endpoints de Autenticación

### Registrar Usuario
```http
POST /auth/register
Content-Type: application/json

{
    "email": "usuario@example.com",
    "username": "nombreusuario",
    "password": "contraseña123"
}
```

### Iniciar Sesión
```http
POST /auth/login
Content-Type: application/json

{
    "email": "usuario@example.com",
    "password": "contraseña123"
}
```

**Respuesta:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

## Endpoints de Películas

### Obtener todas las películas (Público)
```http
GET /movies
```

### Obtener película por ID (Público)
```http
GET /movies/{id}
```

### Filtrar películas por categoría (Público)
```http
GET /movies/?category=Action
```

### Crear película (Requiere Autenticación)
```http
POST /movies
Authorization: Bearer {token}
Content-Type: application/json

{
    "title": "Inception",
    "overview": "Un ladrón que roba secretos corporativos...",
    "year": 2010,
    "rating": 8.8,
    "category": "Sci-Fi"
}
```

### Actualizar película (Requiere Autenticación)
```http
PUT /movies/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
    "title": "Inception - Director's Cut",
    "overview": "Versión extendida del thriller de ciencia ficción...",
    "year": 2010,
    "rating": 9.0,
    "category": "Sci-Fi"
}
```

### Eliminar película (Requiere Autenticación)
```http
DELETE /movies/{id}
Authorization: Bearer {token}
```

## 🔧 Configuración

### Variables de Entorno
Puedes personalizar la configuración modificando los siguientes archivos:

- `config/database.py`: Configuración de base de datos
- `utils/jwt_manager.py`: Configuración del JWT (secret key, tiempo de expiración)

### Configuración JWT
Por defecto, los tokens JWT tienen una duración de 24 horas. Para cambiar esto, modifica:
```python
# utils/jwt_manager.py
expire = datetime.utcnow() + timedelta(hours=24)  # Cambiar aquí
```

## 🗄 Modelos de Datos

### Usuario
```python
{
    "id": "int",
    "email": "string",
    "username": "string",
    "hashed_password": "string"
}
```

### Película
```python
{
    "id": "int",
    "title": "string",
    "overview": "string",
    "year": "int",
    "rating": "float",
    "category": "string"
}
```

## Pruebas de la API

### Con curl
```bash
# Registrar usuario
curl -X POST "http://localhost:8001/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","username":"testuser","password":"123456"}'

# Iniciar sesión
curl -X POST "http://localhost:8001/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"123456"}'

# Crear película (con token)
curl -X POST "http://localhost:8001/movies" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -d '{"title":"Test Movie","overview":"A test movie","year":2024,"rating":8.5,"category":"Action"}'
```

### Con Postman o Thunder Client
1. Importa la colección desde `/docs` (formato OpenAPI)
2. Configura el token JWT en las peticiones protegidas
3. Usa el endpoint de login para obtener el token

## Seguridad

### Características de Seguridad Implementadas:
- **Contraseñas hasheadas**: Usando bcrypt
- **Tokens JWT**: Con expiración de 24 horas
- **Validación de entrada**: Schemas de Pydantic
- **Endpoints protegidos**: Middleware de autenticación
- **Manejo de errores**: Sin exposición de información sensible

### Recomendaciones para Producción:
- Cambiar la clave secreta del JWT
- Usar variables de entorno para configuración sensible
- Implementar rate limiting
- Usar HTTPS
- Configurar CORS apropiadamente

## Solución de Problemas

### Error: Puerto ya en uso
```bash
# Usar un puerto diferente
uvicorn main:app --reload --port 8001
```

### Error: Módulo no encontrado
```bash
# Asegúrate de estar en el directorio correcto
cd basic_movie_api_maria
pip install -r requirements.txt
```

### Error: Base de datos no existe
```bash
# Reinicializar la base de datos
python init_db.py
```

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo `LICENSE` para más detalles.

## Autor

**María Salvador** - Desarrolladora Principal

## Agradecimientos

- FastAPI por el excelente framework
- SQLAlchemy por el ORM robusto
- Pydantic por la validación de datos
- PyJWT por el manejo de tokens

---

**¡Disfruta desarrollando con esta API!**