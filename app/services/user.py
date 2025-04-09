from app.schemas.user import UserPublic, UserPrivate

def user_private_to_public(user_private: UserPrivate) -> UserPublic:
    return UserPublic(username=user_private.username)