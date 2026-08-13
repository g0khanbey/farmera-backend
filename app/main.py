from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine


app = FastAPI(
    title="Farm Era API",
    description="Farm Era oyun sunucusu",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "game": "Farm Era",
        "status": "online",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/db-health")
def database_health():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1")).scalar_one()

    return {
        "database": "connected",
        "result": result,
    }