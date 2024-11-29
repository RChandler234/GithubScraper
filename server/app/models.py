from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UsersModel(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(), unique=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    projects = db.relationship(
        "ProjectsModel", order_by="ProjectsModel.id", back_populates="user"
    )

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return f"<User {self.username}>"


class ProjectsModel(db.Model):
    __tablename__ = "projects"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # TODO: fix naming convention
    userid = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    name = db.Column(db.String())
    description = db.Column(db.String())
    forks = db.Column(db.Integer)
    stars = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user = db.relationship("UsersModel", back_populates="projects")

    def __init__(self, userid, name, description, forks, stars):
        self.userid = userid
        self.name = name
        self.description = description
        self.forks = forks
        self.stars = stars

    def __repr__(self):
        return f"<Project {self.name}>"
