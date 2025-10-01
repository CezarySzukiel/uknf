from schemas.user import User


def get_if_user_exists(user) -> User | None:
    if user:
        return User.model_validate(user)
    return None
