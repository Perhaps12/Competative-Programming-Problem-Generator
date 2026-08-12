from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.connection import Base, engine
from src.database import models  # noqa: F401  (import ensures models register with Base)
from src.routes import meta_routes, execute_routes, problems_routes

app = FastAPI(title="Leetcode Clone API")

# Allow the Next.js frontend to call this API during local dev.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup if they don't exist yet.
Base.metadata.create_all(bind=engine)

app.include_router(meta_routes.router, prefix="/meta", tags=["meta"])
app.include_router(execute_routes.router, prefix="/execute", tags=["execute"])
app.include_router(problems_routes.router, prefix="/problems", tags=["problems"])