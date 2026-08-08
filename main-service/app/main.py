from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    # Используем настройки из .env
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS,
    )

    app.include_router(api_router, prefix="/api/v1")

    return app

app = create_app()