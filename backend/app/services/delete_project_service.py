from sqlalchemy.orm import Session
from app.models.project import Project


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