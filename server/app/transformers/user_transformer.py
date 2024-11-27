def user_transformer(user_model):
    return {
                "username": user_model.username,
                "id": user_model.id,
                "created_at": user_model.created_at
            }