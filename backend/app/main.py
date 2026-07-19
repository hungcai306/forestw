from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.api import admin, administrative, auth, health
from app.core.config import settings
from app.core.database import init_database
from app.services.seed import seed

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    seed()
    yield

app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(administrative.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"name": settings.app_name, "docs": "/docs"}

static_dir = Path("/app/static")
if static_dir.exists():
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="frontend")
