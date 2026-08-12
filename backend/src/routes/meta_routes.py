import os
 
import httpx
from fastapi import APIRouter, HTTPException
 
router = APIRouter()
 
PISTON_URL = os.environ.get("PISTON_URL", "http://localhost:2000")
 
 
@router.get("/health")
async def health():
    """Confirm this API and Piston are both reachable."""
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{PISTON_URL}/api/v2/runtimes", timeout=5)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=503, detail=f"Piston unreachable: {e}")
    return {"status": "ok", "piston": "reachable"}
 
 
@router.get("/languages")
async def list_languages():
    """List all languages/versions currently installed on the Piston instance."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{PISTON_URL}/api/v2/runtimes", timeout=10)
        resp.raise_for_status()
        return resp.json()