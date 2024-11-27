from app import ProjectsModel, db

class ProjectsService:
    @staticmethod
    def get_most_starred_projects(n):
        projects = ProjectsModel.query.all()
        results = [
            {
                "userid": project.userid,
                "name": project.name,
                "description": project.description,
                "forks": project.forks,
                "stars": project.stars
            } for project in projects]

        return {"count": len(results), "projects": results}
    
    @staticmethod
    def create_project(userid, name, description, forks, stars):
        created_project = ProjectsModel(userid, name, description, forks, stars)
        db.session.add(created_project)
        db.session.commit()
        return created_project
    
    @staticmethod
    def scrape_project_data(username):
        print(username)