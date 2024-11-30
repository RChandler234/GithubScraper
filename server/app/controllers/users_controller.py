from flask import Blueprint, jsonify
from app.services.users_services import UsersService
from app.utils.error import ServerException
from flask_restful import Resource


class UsersGETMostRecentResource(Resource):
    def get(self, num_users):
        """
        Get n most recently created users
        ---
        parameters:
          - in: path
            name: num_users
            type: integer
            required: true
        responses:
          200:
            description: List of n most recently created users
          400:
            description: Invalid number of users passed in
          500:
            description: Failed to Fetch Users
        """
        if num_users < 0:
            raise ServerException(
                "Invalid number of users, must be a positive number", 400
            )

        users = UsersService.get_recent_users(num_users)

        return {"users": users}
