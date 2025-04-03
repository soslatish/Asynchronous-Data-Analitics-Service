from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import devices, users, analytics
from app.db.database import Base, engine
from app.core.config import get_settings

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
)

#CORS 
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
app.include_router(devices.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to the {settings.PROJECT_NAME} API",
        "docs": "/docs"
    }

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "healthy"}