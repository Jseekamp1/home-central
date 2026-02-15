from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.features.auth.router import router as auth_router
from app.features.projects.router import router as projects_router

app = FastAPI(title="Home Central API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(projects_router, prefix="/projects", tags=["projects"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
