FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (separate layer -- only re-installs if
# requirements.txt actually changes, speeding up rebuilds).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code.
COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]