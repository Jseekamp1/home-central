from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.features.projects.router import router as projects_router
from app.features.properties.router import router as properties_router
from app.features.steps.router import router as steps_router
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
app.include_router(projects_router, tags=["projects"])
app.include_router(steps_router, tags=["steps"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
