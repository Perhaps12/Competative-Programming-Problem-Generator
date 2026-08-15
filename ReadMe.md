# Competative Programming Problem Generator

An AI-generated coding problem judge with live code execution, built with Next.js, FastAPI, Postgres, and Piston. Supports Python and Java

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js LTS](https://nodejs.org)
- Python 3.12+
- A free [Gemini API key](https://aistudio.google.com/app/apikey)

## Setup (first time only)

1. **Clone/download and unzip** this repository.

2. **Create a Python virtual environment** at the project root:
   ```
   python -m venv venv
   ```

3. **Activate it and install backend dependencies:**
   ```
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Add your Gemini API key.** Create a file named `.env` inside `backend/` containing:
   ```
   API_KEY=your_key_here
   ```

5. **Install frontend dependencies:**
   ```
   cd frontend
   npm install
   cd ..
   ```

6. **Start Docker containers:**
   ```
   docker compose up -d
   ```

7. **Install language runtimes into Piston** (only needed once — a fresh Docker volume starts with none installed):
   ```
   curl -X POST http://127.0.0.1:2000/api/v2/packages -H "Content-Type: application/json" -d "{\"language\":\"python\",\"version\":\"3.10.0\"}"
   ```
   ```
   curl -X POST http://127.0.0.1:2000/api/v2/packages -H "Content-Type: application/json" -d "{\"language\":\"java\",\"version\":\"15.0.2\"}"
   ```

## Running

Once set up, start everything with:
```
run.bat
```
This starts Docker, the backend, and the frontend together.

Then visit **http://localhost:3000**.

## Notes

- Docker containers persist installed language runtimes between restarts, as long as you don't run `docker compose down -v` (the `-v` flag deletes volumes, including installed Piston packages).
- Backend runs on `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.