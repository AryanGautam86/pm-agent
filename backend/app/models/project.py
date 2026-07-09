from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database.db import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)

    tasks = relationship(
        "Task",
        back_populates="project"
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

    status = Column(String, default="Todo")

    # Due date
    due_date = Column(Date, nullable=True)

    # New field: Priority
    priority = Column(String, default="Medium")

    project_id = Column(
        Integer,
        ForeignKey("projects.id")
    )

    project = relationship(
    "Project",
    back_populates="tasks")