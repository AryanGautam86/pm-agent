from datetime import datetime

from sqlalchemy.orm import Session

from app.models.project import Project, Task


def normalize(name: str):
    """
    Normalize project names so that:
    AI Chatbot
    AI Chatbot project
    Project AI Chatbot

    are treated as the same.
    """

    if not name:
        return ""

    return (
        name.lower()
        .replace("project", "")
        .strip()
    )


def create_task(
    db: Session,
    project_name: str,
    task_name: str,
    due_date=None,
    priority="Medium",
):

    # ---------------------------------
    # Find matching project
    # ---------------------------------

    projects = db.query(Project).all()

    project = None

    target = normalize(project_name)

    for p in projects:

        db_name = normalize(p.name)

        if (
            target == db_name
            or target in db_name
            or db_name in target
        ):
            project = p
            break

    if not project:
        return {
            "message": "Project not found."
        }

    # ---------------------------------
    # Check duplicate task
    # ---------------------------------

    existing_task = (
        db.query(Task)
        .filter(
            Task.project_id == project.id,
            Task.title == task_name
        )
        .first()
    )

    if existing_task:
        return {
            "message": "Task already exists."
        }

    # ---------------------------------
    # Parse due date
    # ---------------------------------

    parsed_due_date = None

    if due_date:

        try:
            parsed_due_date = datetime.strptime(
                due_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            parsed_due_date = None

    # ---------------------------------
    # Validate priority
    # ---------------------------------

    valid_priorities = [
        "High",
        "Medium",
        "Low",
    ]

    if priority not in valid_priorities:
        priority = "Medium"

    # ---------------------------------
    # Create task
    # ---------------------------------

    task = Task(
        title=task_name,
        project_id=project.id,
        due_date=parsed_due_date,
        priority=priority,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "message": "Task created successfully.",
        "task": {
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "priority": task.priority,
            "due_date": (
                task.due_date.isoformat()
                if task.due_date
                else None
            ),
            "project": project.name,
        },
    }