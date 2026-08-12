"""
Entry point for the backend server.
Run with: python main.py
"""
 
import uvicorn
 
if __name__ == "__main__":
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)
 