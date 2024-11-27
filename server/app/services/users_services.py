from app import db, UsersModel, ProjectsModel
from app.services.projects_services import ProjectsService

class UsersService:
    @staticmethod
    def get_user_projects(username):
        # TODO: flesh out
        created_user = UsersService.create_user(username)
        created_project = ProjectsService.create_project(created_user.id, "test project", 'test', 1, 1)
        return {"message": f"user {created_project.description} has been created successfully."}
    
    @staticmethod
    def create_user(username):
        new_user = UsersModel(username=username)
        db.session.add(new_user)
        db.session.commit()
        return new_user
        
    
    @staticmethod
    def get_recent_users(n):
        # TODO: flesh out
        users = UsersModel.query.all()
        results = [
            {
                "username": user.username,
                "id": user.id
            } for user in users]

        return {"count": len(results), "users": results}