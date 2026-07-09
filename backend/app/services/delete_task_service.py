from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.project import Task

def delete_task(db: Session, task_name: str):
    task = (
        db.query(Task)
        .filter(Task.title == task_name)
        .first()
    )
    if not task:
        return {
            "message": "Task not found."
        }
    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully."
    }


def delete_project(db: Session, project_name: str):
    project = (
        db.query(Project)
        .filter(Project.name == project_name)
        .first()
    )
    if not project:
        return {
            "message": "Project not found."
        }

    db.delete(project)
    db.commit()
    return {
        "message": "Project deleted successfully."
    }