from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.models.project import Project, Task

from app.services.gemini_service import ask_gemini
from app.services.task_service import create_task
from app.services.update_task_service import update_task_status
from app.services.delete_task_service import delete_task
from app.services.delete_project_service import delete_project
from app.services.update_priority_service import update_task_priority
from app.services.update_due_date_service import update_task_due_date

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(request: ChatRequest):

    print("\n==============================")
    print("User Message:", request.message)

    response = ask_gemini(request.message)

    print("Gemini Response:", response)
    print("==============================")

    # -----------------------------
    # GEMINI ERROR
    # -----------------------------
    if response["intent"] == "ERROR":

        print("Gemini Error:", response["reply"])

        return {
            "message": response["reply"]
        }

    # -----------------------------
    # CREATE PROJECT
    # -----------------------------
    elif response["intent"] == "CREATE_PROJECT":

        db: Session = SessionLocal()

        existing_project = (
            db.query(Project)
            .filter(Project.name == response["project_name"])
            .first()
        )

        if existing_project:
            db.close()
            return {
                "message": "Project already exists."
            }

        project = Project(
            name=response["project_name"]
        )

        db.add(project)
        db.commit()
        db.refresh(project)

        db.close()

        return {
            "message": "Project created successfully.",
            "project": {
                "id": project.id,
                "name": project.name
            }
        }

    # -----------------------------
    # CREATE TASK
    # -----------------------------
    elif response["intent"] == "CREATE_TASK":

        db = SessionLocal()

        result = create_task(
            db,
            response["project_name"],
            response["task_name"],
            response.get("due_date"),
            response.get("priority", "Medium")
        )

        print("Task Result:", result)

        db.close()

        return result

    # -----------------------------
    # UPDATE TASK STATUS
    # -----------------------------
    elif response["intent"] == "UPDATE_TASK_STATUS":

        db = SessionLocal()

        result = update_task_status(
            db,
            response["task_name"],
            response["status"]
        )

        print("Update Status:", result)

        db.close()

        return result

    # -----------------------------
    # UPDATE TASK PRIORITY
    # -----------------------------
    elif response["intent"] == "UPDATE_TASK_PRIORITY":

        db = SessionLocal()

        result = update_task_priority(
            db,
            response["task_name"],
            response["priority"]
        )

        print("Update Priority:", result)

        db.close()

        return result

    # -----------------------------
    # UPDATE TASK DUE DATE
    # -----------------------------
    elif response["intent"] == "UPDATE_TASK_DUE_DATE":

        db = SessionLocal()

        result = update_task_due_date(
            db,
            response["task_name"],
            response["due_date"]
        )

        print("Update Due Date:", result)

        db.close()

        return result

    # -----------------------------
    # DELETE TASK
    # -----------------------------
    elif response["intent"] == "DELETE_TASK":

        db = SessionLocal()

        result = delete_task(
            db,
            response["task_name"]
        )

        print("Delete Task:", result)

        db.close()

        return result

    # -----------------------------
    # DELETE PROJECT
    # -----------------------------
    elif response["intent"] == "DELETE_PROJECT":

        db = SessionLocal()

        result = delete_project(
            db,
            response["project_name"]
        )

        print("Delete Project:", result)

        db.close()

        return result

    # -----------------------------
    # NORMAL CHAT
    # -----------------------------
    else:

        return {
            "message": response.get(
                "reply",
                "Sorry, I couldn't understand your request."
            )
        }


# ==================================================
# GET ALL PROJECTS
# ==================================================

@router.get("/projects")
def get_projects():

    db = SessionLocal()

    projects = db.query(Project).all()

    result = []

    for project in projects:
        result.append({
            "id": project.id,
            "name": project.name,
            "description": project.description,
        })

    db.close()

    return result


# ==================================================
# GET ALL TASKS
# ==================================================

@router.get("/tasks")
def get_tasks():

    db = SessionLocal()

    tasks = db.query(Task).all()

    result = []

    for task in tasks:
        result.append({
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "priority": task.priority,
            "due_date": (
                task.due_date.isoformat()
                if task.due_date
                else None
            ),
            "project_id": task.project_id,
        })

    db.close()

    return result


# ==================================================
# GET TASKS OF A PROJECT
# ==================================================

@router.get("/projects/{project_id}/tasks")
def get_project_tasks(project_id: int):

    db = SessionLocal()

    tasks = (
        db.query(Task)
        .filter(Task.project_id == project_id)
        .all()
    )

    result = []

    for task in tasks:
        result.append({
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "priority": task.priority,
            "due_date": (
                task.due_date.isoformat()
                if task.due_date
                else None
            ),
        })

    db.close()

    return result