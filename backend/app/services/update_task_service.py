from sqlalchemy.orm import Session
from app.models.project import Task


def update_task_status(db: Session, task_name: str, status: str):

    task = (
        db.query(Task)
        .filter(Task.title == task_name)
        .first()
    )

    if not task:
        return {
            "message": "Task not found."
        }

    task.status = status

    db.commit()
    db.refresh(task)

    return {
        "message": f"Task marked as {status}."
    }