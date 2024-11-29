from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flasgger import Swagger
from app.utils.custom_api import Api
from flask_restful import Api
from app.models import db
from dotenv import load_dotenv
import os

migrate = Migrate()


def run_server():
    app = Flask(__name__)
    api = Api(app)
    swagger = Swagger(app)

    load_dotenv()
    CLIENT_URL = os.getenv("CLIENT_URL")
    DATABASE_URL = os.getenv("DATABASE_URL")

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app, resources={r"/*": {"origins": CLIENT_URL}})

    from app.utils.error import (
        ServerException,
        handle_custom_exception,
        handle_internal_exception,
        handle_not_found_error,
    )
    from app.controllers.projects_controller import (
        ProjectsGETByUsernameResource,
        ProjectsGETMostStarredResource,
    )
    from app.controllers.users_controller import UsersGETMostRecentResource

    @app.route("/")
    def root():
        return "Welcome to GithubScraper!"

    api.add_resource(
        ProjectsGETMostStarredResource, "/projects/most-starred/<int:num_projects>"
    )
    api.add_resource(
        ProjectsGETByUsernameResource, "/projects/username/<string:username>"
    )
    api.add_resource(UsersGETMostRecentResource, "/users/most-recent/<int:num_users>")

    app.register_error_handler(404, handle_not_found_error)
    app.register_error_handler(ServerException, handle_custom_exception)
    app.register_error_handler(500, handle_internal_exception)

    app.run(host="0.0.0.0", port=5000)
