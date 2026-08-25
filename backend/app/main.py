from fastapi import FastAPI

app = FastAPI(
    title="Financial Tracker API",
    description="Local personal finance tracker backend",
    version="0.1.0",
)


# Health check endpoint
@app.get("/api/health")
def health_check():
    return {"status": "ok"}