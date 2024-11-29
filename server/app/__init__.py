from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flasgger import Swagger
from app.utils.custom_api import Api
from flask_restful import Api
from app.models import db

migrate = Migrate()

def run_server():
    app = Flask(__name__)
    api = Api(app)
    swagger = Swagger(app)

    # TODO: env var
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://postgres@localhost:5432/postgres"

    db.init_app(app)
    migrate.init_app(app, db)

    # TODO: env var
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    from app.utils.error import ServerException, handle_custom_exception, handle_internal_exception, handle_not_found_error
    from app.controllers.projects_controller import ProjectsGETByUsernameResource, ProjectsGETMostStarredResource
    from app.controllers.users_controller import UsersGETMostRecentResource

    @app.route("/")
    def root():
        return "Welcome to GithubScraper!"

    api.add_resource(ProjectsGETMostStarredResource, '/projects/most-starred/<int:num_projects>')
    api.add_resource(ProjectsGETByUsernameResource, '/projects/username/<string:username>' )
    api.add_resource(UsersGETMostRecentResource,'/users/most-recent/<int:num_users>')

    app.register_error_handler(404, handle_not_found_error)
    app.register_error_handler(ServerException, handle_custom_exception)
    app.register_error_handler(500, handle_internal_exception)

    app.run(host="0.0.0.0", port=5000)

