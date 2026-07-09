from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.database.db import Base, engine
from app.models.project import Project

app = FastAPI(title="PM Agent")

# ------------------------------------
# Create database tables
# ------------------------------------
Base.metadata.create_all(bind=engine)

# ------------------------------------
# CORS
# ------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # OK since frontend and backend share the same origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------
# API Routes
# ------------------------------------
app.include_router(router)

# ------------------------------------
# React Build Location
# ------------------------------------
BASE_DIR = Path(__file__).resolve().parent

# ../frontend/dist
FRONTEND_DIST = BASE_DIR.parent / "frontend" / "dist"

# ------------------------------------
# Serve React Assets
# ------------------------------------
assets_dir = FRONTEND_DIST / "assets"

if assets_dir.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=assets_dir),
        name="assets",
    )

# ------------------------------------
# Home Page
# ------------------------------------
@app.get("/", include_in_schema=False)
async def serve_frontend():
    index_file = FRONTEND_DIST / "index.html"

    if index_file.exists():
        return FileResponse(index_file)

    return {"message": "Frontend not built."}

# ------------------------------------
# React Router
# ------------------------------------
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_react(full_path: str):

    # Don't intercept API/docs routes
    if full_path.startswith(("chat", "projects", "tasks", "docs", "redoc", "openapi.json")):
        return {"detail": "Not Found"}

    index_file = FRONTEND_DIST / "index.html"

    if index_file.exists():
        return FileResponse(index_file)

    return {"message": "Frontend not built."}

# ------------------------------------
# Run locally
# ------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )