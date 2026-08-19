import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.connection import Base, engine
from src.database import models  # noqa: F401  (import ensures models register with Base)
from src.routes import meta_routes, execute_routes, problems_routes

app = FastAPI(title="Leetcode Clone API")

# Allow the frontend to call this API. Includes localhost for local dev,
# plus the production domain (read from FRONTEND_URL, set in docker-compose
# via the DOMAIN env var) so this doesn't need to be hardcoded per-environment.
frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", frontend_url],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup if they don't exist yet.
# Fine for a small local project; a real migration tool (Alembic) is the
# better long-term approach once the schema starts changing often.
Base.metadata.create_all(bind=engine)

app.include_router(meta_routes.router, prefix="/meta", tags=["meta"])
app.include_router(execute_routes.router, prefix="/execute", tags=["execute"])
app.include_router(problems_routes.router, prefix="/problems", tags=["problems"])