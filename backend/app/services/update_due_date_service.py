from datetime import datetime

from sqlalchemy.orm import Session

from app.models.project import Task


def update_task_due_date(
    db: Session,
    task_name: str,
    due_date: str
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

    try:
        parsed_date = datetime.strptime(
            due_date,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        return {
            "message": "Invalid date format."
        }

    task.due_date = parsed_date

    db.commit()
    db.refresh(task)

    return {
        "message": "Due date updated successfully.",
        "task": {
            "title": task.title,
            "due_date": task.due_date.isoformat()
        }
    }