from fastapi import FastAPI

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
    return {
        "status": "healthy",
    }