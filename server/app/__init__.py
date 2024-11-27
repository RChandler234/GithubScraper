from flask import Flask, request
from sqlalchemy.dialects.postgresql import UUID
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://postgres@localhost:5432/postgres"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UsersModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(), unique=True)
    projects = db.relationship("ProjectsModel", order_by="ProjectsModel.id", back_populates="user")


    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return f"<User {self.username}>"
    
class ProjectsModel(db.Model):
    __tablename__ = 'projects'
   
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    name = db.Column(db.String())
    description = db.Column(db.String())
    forks = db.Column(db.Integer)
    stars = db.Column(db.Integer)
    user = db.relationship("UsersModel", back_populates="projects")

    def __init__(self, userid, name, description, forks, stars):
        self.userid = userid
        self.name = name
        self.description = description
        self.forks = forks
        self.stars = stars

    def __repr__(self):
        return f"<Project {self.name}>"


@app.route("/")
def root():
    return "Welcome to GithubScraper!"

from app.controllers.projects_controller import projects
from app.controllers.users_controller import users

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(projects, url_prefix='/projects')

