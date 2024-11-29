from flask import Blueprint, jsonify
from app.services.users_services import UsersService
import re
from app.utils.error import ServerException
from flask_restful import Resource


class UsersGETMostRecentResource(Resource):
    def get(self, num_users):
        if num_users < 0:
            raise ServerException("Invalid number of users, must be a positive number")

        users = UsersService.get_recent_users(num_users)

        return {"users": users}
