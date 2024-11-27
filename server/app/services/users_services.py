from app import db, UsersModel, ProjectsModel
from app.services.projects_services import ProjectsService
from app.transformers.user_transformer import user_transformer

class UsersService:
    @staticmethod
    def get_user_projects(username):
        user = UsersService.get_user(username)
        projects = []
        if(not user):
            user = UsersService.create_user(username)
            projects_data = ProjectsService.scrape_project_data(username)
            for project in projects_data:
                created_project = ProjectsService.create_project(user.id, project["repo_name"], project["repo_description"], project["repo_forks"], project["repo_stars"])
                projects.append(created_project)
        else:
            projects = ProjectsService.get_projects_by_user_id(user.id)

        return {"projects": projects}
    
    @staticmethod
    def get_user(username):
        user = UsersModel.query.filter(UsersModel.username == username).first()
        return user
    
    @staticmethod
    def create_user(username):
        new_user = UsersModel(username=username)
        db.session.add(new_user)
        db.session.commit()
        return new_user
        
    
    @staticmethod
    def get_recent_users(n):
        users = UsersModel.query.order_by(UsersModel.created_at.desc()).limit(n)
        results = [user_transformer(user) for user in users]
        return { "users": results}