from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ProjectStatus(str, Enum):
    planning = "planning"
    in_progress = "in_progress"
    completed = "completed"


class ProjectPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class InstructionStep(BaseModel):
    step: int = Field(..., ge=1)
    text: str = Field(..., min_length=1)


class MaterialItem(BaseModel):
    name: str = Field(..., min_length=1)
    quantity: float = Field(default=1, ge=0)
    cost: Optional[float] = Field(default=None, ge=0)
    owned: bool = False


class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.planning
    priority: ProjectPriority = ProjectPriority.medium
    estimated_duration_hours: Optional[float] = Field(default=None, ge=0)
    estimated_cost: Optional[float] = Field(default=None, ge=0)
    instructions: list[InstructionStep] = Field(default_factory=list)
    materials: list[MaterialItem] = Field(default_factory=list)


class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    priority: Optional[ProjectPriority] = None
    estimated_duration_hours: Optional[float] = Field(default=None, ge=0)
    estimated_cost: Optional[float] = Field(default=None, ge=0)
    instructions: Optional[list[InstructionStep]] = None
    materials: Optional[list[MaterialItem]] = None


class ProjectResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    status: ProjectStatus
    priority: ProjectPriority
    estimated_duration_hours: Optional[float] = None
    estimated_cost: Optional[float] = None
    instructions: list[InstructionStep] = Field(default_factory=list)
    materials: list[MaterialItem] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
