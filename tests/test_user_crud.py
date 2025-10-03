import pytest
from crud.user import get_user_by_username, get_user_by_email, create_user, get_user_by_id, update_user, \
    get_all_users, update_user_role, update_user_status, add_user_permission, remove_user_permission, delete_user
from schemas.user import UserCreate, Role, UserUpdate, Permission
from core.rbac import get_permissions_for_role


def test_get_user_by_username(test_users, db):
    user = get_user_by_username("user1", db)
    assert user.username == "user1"


def test_get_user_by_email(test_users, db):
    user = get_user_by_email("user@example.com", db)
    assert user.email == "user@example.com"


def test_create_user(db):
    user_data = UserCreate(
        username="newuser",
        email="newuser@example.com",
        password="newpassword123",
        role=Role.USER
    )
    user = create_user(user_data, db)
    assert user.id == 1
    assert user.username == "newuser"
    assert user.email == "newuser@example.com"
    assert user.role == "user"
    assert user.disabled is False
    assert user.password_hash != "newpassword123"
    assert isinstance(user.permissions, list)


def test_get_user_bu_id(test_users, db):
    user = get_user_by_id(1, db)
    assert user.id == 1


def test_update_user_username(test_users, db):
    user = get_user_by_username("user1", db)
    user_to_save = UserUpdate(username="updateduser")
    updated_user = update_user(user.id, user_to_save, db)
    updated_user_ = get_user_by_id(user.id, db)
    assert updated_user.username == "updateduser"
    assert updated_user == updated_user_


def test_update_user_email(test_users, db):
    user = get_user_by_email("user@example.com", db)
    user_to_save = UserUpdate(email="new@email.com")
    updated_user = update_user(user.id, user_to_save, db)
    updated_user_ = get_user_by_id(user.id, db)
    assert updated_user.email == "new@email.com"
    assert updated_user == updated_user_


def test_update_user_password(test_users, db):
    user = get_user_by_id(1, db)
    old_hashed_password = user.password_hash
    user_to_save = UserUpdate(password="newpassword123")
    updated_user = update_user(user.id, user_to_save, db)
    updated_user_ = get_user_by_id(user.id, db)
    assert updated_user.password_hash != old_hashed_password
    assert updated_user == updated_user_


def test_update_user_username_to_existing(test_users, db):
    user = get_user_by_username("user1", db)
    user_to_save = UserUpdate(username="manager1")
    with pytest.raises(ValueError) as excinfo:
        update_user(user.id, user_to_save, db)
    assert "Username already exists" in str(excinfo.value)


def test_update_user_email_to_existing(test_users, db):
    user = get_user_by_email("user@example.com", db)
    user_to_save = UserUpdate(email="manager@example.com")
    with pytest.raises(ValueError) as excinfo:
        update_user(user.id, user_to_save, db)
    assert "Email already exists." in str(excinfo.value)


def test_get_all_useres(test_users, db):
    users = get_all_users(db)
    assert len(users) == 3


def test_update_user_role(test_users, db):
    user = get_user_by_username("user1", db)
    updated_user = update_user_role(user.id, Role.MANAGER, db)
    update_user_ = get_user_by_id(user.id, db)
    assert updated_user.role == Role.MANAGER == update_user_.role
    assert updated_user.permissions == get_permissions_for_role(Role.MANAGER) == update_user_.permissions


def test_update_user_status(test_users, db):
    user = get_user_by_id(1, db)
    result = update_user_status(user.id, True, db)
    updated_user_ = get_user_by_id(user.id, db)
    assert result is True
    assert updated_user_.disabled is True
    result = update_user_status(user.id, False, db)
    updated_user_ = get_user_by_id(user.id, db)
    assert result is True
    assert updated_user_.disabled is False


def test_add_user_permission(test_users, db):
    user = get_user_by_id(1, db)
    permission = "custom_permission"
    updated_user = add_user_permission(user.id, permission, db)
    updated_user_ = get_user_by_id(user.id, db)
    assert permission in updated_user.permissions
    assert updated_user == updated_user_


def test_remove_user_permission(test_users, db):
    user = get_user_by_id(3, db)  # admin user
    permission_to_remove = Permission.DELETE_USER
    assert permission_to_remove in user.permissions
    updated_user = remove_user_permission(user.id, permission_to_remove, db)
    updated_user_ = get_user_by_id(user.id, db)
    assert permission_to_remove not in updated_user.permissions
    assert updated_user == updated_user_


def test_delete_user(test_users, db):
    user = get_user_by_id(1, db)
    result = delete_user(user.id, db)
    assert result is True
    deleted_user = get_user_by_id(user.id, db)
    assert deleted_user is None


def test_delete_last_admin(test_users, db):
    admin_user = get_user_by_username("admin1", db)
    result = delete_user(admin_user.id, db)
    assert result is False
    existing_admin = get_user_by_id(admin_user.id, db)
    assert existing_admin is not None
