from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.features.properties.router import router as properties_router
from app.features.users.router import router as users_router

app = FastAPI(title="Home Central API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, tags=["users"])
app.include_router(properties_router, prefix="/properties", tags=["properties"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
