from fastapi import FastAPI
from sqlalchemy import text
from app.db.database import engine

app = FastAPI(
    title="Finance API",
    description="Local personal finance tracker backend",
    version="0.1.0",
)


# Health check endpoint
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/health/db")
def database_health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok"}

