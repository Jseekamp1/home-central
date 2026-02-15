from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from app.features.projects.models import ProjectCreate, ProjectResponse, ProjectUpdate
from app.shared.dependencies import get_authenticated_client, get_current_user

router = APIRouter()


@router.post("", response_model=ProjectResponse)
def create_project(
    body: ProjectCreate,
    user: dict = Depends(get_current_user),
    db: Client = Depends(get_authenticated_client),
):
    data = body.model_dump(mode="json")
    data["user_id"] = user["id"]

    result = db.table("projects").insert(data).execute()
    return result.data[0]


@router.get("", response_model=list[ProjectResponse])
def list_projects(db: Client = Depends(get_authenticated_client)):
    result = db.table("projects").select("*").execute()
    return result.data


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, db: Client = Depends(get_authenticated_client)):
    result = db.table("projects").select("*").eq("id", project_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Project not found")
    return result.data[0]


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: str,
    body: ProjectUpdate,
    db: Client = Depends(get_authenticated_client),
):
    existing = db.table("projects").select("*").eq("id", project_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = body.model_dump(exclude_unset=True, mode="json")
    result = db.table("projects").update(update_data).eq("id", project_id).execute()
    return result.data[0]


@router.delete("/{project_id}")
def delete_project(project_id: str, db: Client = Depends(get_authenticated_client)):
    existing = db.table("projects").select("*").eq("id", project_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Project not found")

    db.table("projects").delete().eq("id", project_id).execute()
    return {"message": "Project deleted"}
