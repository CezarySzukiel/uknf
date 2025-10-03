from crud.auth import authenticate_user
from crud.user import get_user_by_id


def test_authenticate_user(test_users, db):
    user = get_user_by_id(1, db)
    authenticated_user = authenticate_user(user.username, "password123", db)
    assert user == authenticated_user
