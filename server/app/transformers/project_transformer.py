def project_transformer(project_model):
    return {
                "userid": project_model.userid,
                "name": project_model.name,
                "description": project_model.description,
                "forks": project_model.forks,
                "stars": project_model.stars,
                "created_at": project_model.created_at
            } 