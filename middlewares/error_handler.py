from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging


class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": True,
                    "message": exc.detail,
                    "status_code": exc.status_code
                }
            )
        except ValueError as exc:
            return JSONResponse(
                status_code=400,
                content={
                    "error": True,
                    "message": f"Validation error: {str(exc)}",
                    "status_code": 400
                }
            )
        except Exception as exc:
            logging.error(f"Unhandled exception: {str(exc)}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": True,
                    "message": "Internal server error",
                    "status_code": 500
                }
            )
