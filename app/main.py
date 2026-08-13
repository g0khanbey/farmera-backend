from fastapi import FastAPI
from sqlalchemy import text

from app.api.auth import router as auth_router
from app.api.players import router as players_router
from app.db.session import engine
from app.api.inventory import router as inventory_router

app = FastAPI(
    title="Farm Era API",
    description="Farm Era oyun sunucusu",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(players_router)
app.include_router(inventory_router)

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