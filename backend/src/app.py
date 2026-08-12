from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
from src.routes import meta_routes, execute_routes
 
app = FastAPI(title="Leetcode Clone API")
 
# Allow the Next.js frontend to call this API during local dev.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
 
app.include_router(meta_routes.router, prefix="/meta", tags=["meta"])
app.include_router(execute_routes.router, prefix="/execute", tags=["execute"])