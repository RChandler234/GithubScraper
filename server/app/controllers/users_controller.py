from flask import Blueprint, jsonify
from app.services.users_services import UsersService
import re
from app.utils.error import ServerException


users = Blueprint('users', __name__)

GITHUB_USERNAME_REGEX = re.compile("^[a-zA-Z0-9-]+$")

@users.route('/projects/<string:username>',  methods=["GET"])
def get_user_projects(username):
    if not GITHUB_USERNAME_REGEX.match(username):
        raise ServerException( "Invalid Username. Must only contain alphanumeric characters or -", 400)

    if len(username) < 1 or len(username) > 39:
        raise ServerException("Invalid Username. Must be between 1 and 39 characters long", 400)
    
    projects = UsersService.find_user_projects(username)
    
    return {"projects": projects}
    
@users.route('/most-recent/<int:num_users>',  methods=["GET"])
def get_recent_users(num_users):
    if num_users < 0:
        raise ServerException("Invalid number of users, must be a positive number")
    
    users = UsersService.get_recent_users(num_users)

    return {"users": users}
