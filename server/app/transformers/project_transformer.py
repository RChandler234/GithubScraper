def project_transformer(project_model):
    """
    Transforms the Project type returned by the database into a type into a serializable dict
    """
    return {
        "id": str(project_model.id),
        "user_id": str(project_model.user_id),
        "name": project_model.name,
        "description": project_model.description,
        "forks": project_model.forks,
        "stars": project_model.stars,
        "created_at": project_model.created_at.isoformat(),
        "username": project_model.user.username,
    }
