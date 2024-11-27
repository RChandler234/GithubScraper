from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return "Welcome to GithubScraper!"

from app.controllers.projects_controller import projects
from app.controllers.users_controller import users

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(projects, url_prefix='/projects')

