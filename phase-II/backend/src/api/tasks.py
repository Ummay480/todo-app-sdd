from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
import uuid
from src.database import get_session
from src.models.task import Task, TaskCreate, TaskUpdate
from src.services.task_service import TaskService
from src.auth.jwt_handler import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[Task])
async def list_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = Query(None),
    sort_by: str = "created_at",
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return TaskService.get_tasks(
        session,
        uuid.UUID(current_user["id"]),
        status,
        priority,
        search,
        sort_by
    )

@router.post("/", response_model=Task, status_code=201)
async def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return TaskService.create_task(session, task, uuid.UUID(current_user["id"]))

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: uuid.UUID,
    task: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    db_task = TaskService.update_task(session, task_id, task, uuid.UUID(current_user["id"]))
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    task = TaskService.get_task_by_id(session, task_id, uuid.UUID(current_user["id"]))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}/complete", response_model=Task)
async def toggle_task_completion(
    task_id: uuid.UUID,
    completed: bool,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    task = TaskService.update_task_completion(session, task_id, completed, uuid.UUID(current_user["id"]))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    success = TaskService.delete_task(session, task_id, uuid.UUID(current_user["id"]))
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
