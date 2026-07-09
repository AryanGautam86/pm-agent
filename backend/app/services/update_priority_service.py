from sqlalchemy.orm import Session

from app.models.project import Task


def update_task_priority(
    db: Session,
    task_name: str,
    priority: str
):

    task = (
        db.query(Task)
        .filter(Task.title.ilike(task_name))
        .first()
    )

    if not task:
        return {
            "message": "Task not found."
        }

    valid_priorities = [
        "High",
        "Medium",
        "Low",
    ]

    if priority not in valid_priorities:
        return {
            "message": "Invalid priority."
        }

    task.priority = priority

    db.commit()
    db.refresh(task)

    return {
        "message": f"Priority updated to {priority}.",
        "task": {
            "title": task.title,
            "priority": task.priority
        }
    }