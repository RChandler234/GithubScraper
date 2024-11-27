from flask import Blueprint, request
from app.services.users_services import UsersService

users = Blueprint('users', __name__)

@users.route('/projects/<username>',  methods=["GET"])
def get_user_projects(username):
    # TODO: input validation
    return UsersService.get_user_projects(username)
    
@users.route('/most-recent/<num_users>',  methods=["GET"])
def get_recent_users(num_users):
    # TODO: input validation
    return UsersService.get_recent_users(num_users)
