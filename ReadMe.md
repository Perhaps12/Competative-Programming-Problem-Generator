**Demo Video:** https://youtu.be/kao_LyX6fkM?si=PDVM6WbH8zl7asa

# Competitive Programming Problem Generator

An AI-generated coding problem judge with live code execution, built with Next.js, FastAPI, Postgres, and Piston. Supports Python and Java.

## Deployment

This project was deployed on AWS EC2 using Docker, with the app stack running
in containers behind a Caddy reverse proxy (automatic HTTPS). The live instance
has since been shut down to avoid hosting costs.

## Project overview

- Frontend: Next.js app
- Backend: FastAPI API
- Database: Postgres
- Code execution: Piston
- AI generation: Gemini API

> Local development setup is the fallback if the website is down because the EC2 container has stopped. In that case, run the app locally using the instructions below to continue working without the hosted deployment.

---

## Local development setup

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js LTS](https://nodejs.org)
- Python 3.12+
- A free [Gemini API key](https://aistudio.google.com/app/apikey)

### First-time setup

1. Clone/download and unzip this repository.

2. Create a Python virtual environment at the project root:
   ```
   python -m venv venv
   ```

3. Activate it and install the backend dependencies:
   ```
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Create a `.env` file at the project root if you want to run the full Docker setup, using the provided example as a template:
   ```
   copy .env.example .env
   ```
   Then update the values as needed. At minimum you should set:
   ```
   POSTGRES_USER=your_postgres_user
   POSTGRES_PASSWORD=your_postgres_password
   POSTGRES_DB=your_database_name
   API_KEY=your_gemini_api_key
   DOMAIN=localhost
   ```
   If you are running locally, set `DOMAIN=localhost` unless you also want to mirror the EC2/Caddy setup.

5. If you are running the backend directly (outside Docker), create a `.env` inside `backend/` with the API key as well:
   ```
   API_KEY=your_gemini_api_key
   ```

6. Install frontend dependencies:
   ```
   cd frontend
   npm install
   cd ..
   ```

7. Start the Docker services:
   ```
   docker compose up -d
   ```

8. Install the required language runtimes into Piston. This is needed once for a fresh Docker volume:
   ```
   curl -X POST http://127.0.0.1:2000/api/v2/packages -H "Content-Type: application/json" -d "{\"language\":\"python\",\"version\":\"3.10.0\"}"
   ```
   ```
   curl -X POST http://127.0.0.1:2000/api/v2/packages -H "Content-Type: application/json" -d "{\"language\":\"java\",\"version\":\"15.0.2\"}"
   ```

### Running locally

Once set up, start everything with:
```bat
run.bat
```
This starts Docker, the backend, and the frontend together.

Then open:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

### Adjustments you may need for local work

- The frontend defaults to `http://localhost:8000` for the backend API in `frontend/lib/api.ts`. If you are hosting the API somewhere else, set a local environment variable in `frontend/.env.local`:
  ```
  NEXT_PUBLIC_API_URL=http://localhost:8000
  ```

- If you are running the app without Docker, make sure the backend environment includes `API_KEY` and that the database is available. For a local Postgres instance, update the connection string in your environment to match your machine.

- If you want to test the production-style Caddy setup locally, set `DOMAIN` in the project root `.env` to a valid local hostname or custom domain, and ensure your machine can resolve it. Otherwise, the default local URLs above are the easiest option.

- If you stop Docker and run `docker compose down -v`, the Postgres and Piston volumes are deleted, and you will need to reinstall the Piston language packages again.

- On Windows, the included `run.bat` script expects the project to have a virtual environment named `venv` in the repository root. If you use a different Python environment name or shell, activate it manually before running the backend.

---

## Notes

- Docker containers persist installed language runtimes between restarts, as long as you do not run `docker compose down -v`.
- The EC2 deployment uses the same application structure as the local version, but it adds a public domain and uses Caddy to route traffic to the frontend and backend services.
- The app is designed to support both local development and a production deployment behind a public hostname, such as the AWS EC2 deployment at https://13-58-28-162.nip.io/.
