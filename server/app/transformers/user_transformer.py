def user_transformer(user_model):
    """
    Transforms the User type returned by the database into a serializable dict
    """
    return {
        "username": user_model.username,
        "id": str(user_model.id),
        "created_at": user_model.created_at.isoformat(),
    }
